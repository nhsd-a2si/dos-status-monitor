import datetime
import time
import redis
from rq import Queue

from dos_status_monitor import database, uec_dos, config, slack, logger, sms
from dos_status_monitor import utils

# Set up RQ queue
conn = redis.from_url(config.REDIS_URL)
q = Queue(connection=conn)


def update_status_from_service_data(service_data):

    status = {
        'id': service_data['id'],
        'name': service_data['name'],
        'type': service_data['type']['name'],
        'postCode': service_data['postcode'],
        'easting': service_data['easting'],
        'northing': service_data['northing'],
        'lastUpdatedTime': datetime.datetime.utcnow(),
        'capacity': service_data['capacity']['status']['human'],
        'rag': service_data['capacity']['status']['rag'],
        'source': config.APP_NAME
    }

    database.update_status(status)


def update_status_from_latest_snapshot(service_id):

    snapshot = database.get_most_recent_snapshot_for_service(service_id)

    status = {
        'id': snapshot['id'],
        'name': snapshot['name'],
        'type': snapshot['type'],
        'postCode': snapshot['postCode'],
        'easting': snapshot['easting'],
        'northing': snapshot['northing'],
        'lastUpdatedTime': datetime.datetime.utcnow(),
        'capacity': snapshot['capacity']['status'],
        'rag': snapshot['capacity']['rag'],
        'source': config.APP_NAME
    }

    database.update_status(status)


def store_snapshot(service):
    if service['capacity']['status']['human']:
        logger.debug(f"{service['name']} - {service['capacity']['status']['human']}")

    snapshot = {
        'id': service['id'],
        'name': service['name'],
        'type': service['type']['name'],
        'postCode': service['postcode'],
        'easting': int(service['easting']),
        'northing': int(service['northing']),
        'snapshotTime': datetime.datetime.utcnow(),
        'capacity': {
            'status': service['capacity']['status']['human'],
            'rag': service['capacity']['status']['rag'],
        },
        'source': config.APP_NAME
    }

    database.add_snapshot(snapshot)


def is_robot_change(old_status, new_status):
    if old_status == 'HIGH' and new_status == '':
        return True
    else:
        return False


def has_status_changed(service_id):

    logger.debug(f'Checking status for {service_id}')

    status = database.get_status_for_single_service(service_id)

    if status:
        old_status = status['capacity']
        old_rag = status['rag']

    elif not status:
        service_data = uec_dos.get_service_by_service_id(service_id)
        logger.warn("No status for this service - adding a status entry")
        update_status_from_service_data(service_data)
        return

    service_snapshot = database.get_most_recent_snapshot_for_service(service_id)

    new_status = service_snapshot['capacity']['status']

    if service_snapshot:

        logger.debug(f'Previous Status: {old_status}, '
                     f'New Status: {new_status}')

        if old_status == new_status:
            logger.debug(f"Status for {service_id} hasn't changed")
            update_status_from_latest_snapshot(service_id)
            return

        elif old_status != new_status:

            if is_robot_change(old_status, new_status):
                logger.info("Skipping change as it's just the 24h ROBOT")
                return

            # Retrieve the entire service record from the DoS as this
            # contains details of the person who changed the status
            service_data = uec_dos.get_service_by_service_id(service_id)

            service_updated_by = service_data['capacity']['updated']['by']
            service_status = service_data['capacity']['status']['human']
            service_rag = service_data['capacity']['status']['rag']
            service_name = service_data['name']
            service_postcode = service_data['postcode']
            service_updated_date = service_data['capacity']['updated']['date']
            service_updated_time = service_data['capacity']['updated']['time']
            service_region = service_data['region']['name']
            service_type = service_data['type']['name']

            logger.info(f"Status has changed for {service_id} - "
                        f"{service_name} - {service_status} "
                        f"({service_rag})")

            # Fix the incorrect service_updated_time by subtracting an hour from the supplied time.
            # Below line needs to be included when in BST
            # TODO: Remove this fix when the API is fixed to return the correct local time
            service_updated_time, service_updated_date = utils.adjust_timestamp_for_api_bst_bug(service_updated_time,
                                                                                                service_updated_date)

            document = {'id': service_id,
                        'name': service_name,
                        'type': service_type,
                        'postCode': service_postcode,
                        'region': service_region,
                        'eventTime': datetime.datetime.utcnow(),
                        'capacity': {
                            'newStatus': service_status,
                            'newRag': service_rag,
                            'previousStatus': old_status,
                            'previousRag': old_rag,
                            'changedBy': service_updated_by,
                            'changedDate': service_updated_date,
                            'changedTime': service_updated_time
                        },
                        'source': config.APP_NAME
                        }

            database.add_change(document)

            update_status_from_service_data(service_data)

            if config.SMS_ENABLED:
                q.enqueue(sms.send_sms, config.MOBILE_NUMBER,
                          f"{service_name} ({service_id}) in {service_region} "
                          f"changed to {service_status} ({service_rag}) by "
                          f"{service_updated_by} at {service_updated_time}.",
                          at_front=True)

            if config.SLACK_ENABLED:
                q.enqueue(slack.send_slack_notification,
                          service_name,
                          service_region,
                          service_status,
                          old_status,
                          service_type,
                          service_updated_time,
                          service_updated_by,
                          at_front=True)

            return


def snapshot_service_search(probe):
    postcode = probe['postcode']
    search_distance = probe['search_distance']
    service_types = probe['service_types']
    number_per_type = probe['number_per_type']
    gp = probe['gp']
    search_role = probe['search_role']

    try:
        start = time.time()
        services = uec_dos.get_services_by_service_search(postcode,
                                                          search_distance,
                                                          service_types,
                                                          number_per_type,
                                                          gp,
                                                          search_role)
        round_trip = time.time() - start

        logger.info(f"Ran probe for {postcode} as {search_role}, at {search_distance} "
                    f"miles, for {number_per_type} each of service types: "
                    f"{service_types} - {len(services)} services (Took {round_trip})")

        for service in services:

            store_snapshot(service)

            service_id = service['id']

            # Only store snapshots and queue status checks if the status has a value
            if service['capacity']['status']['human'] != "":
                logger.debug('Queueing capacity check for {service_id}')

                q.enqueue(has_status_changed,
                          service_id)
            else:
                logger.debug("Empty capacity - skipping status check")
                update_status_from_latest_snapshot(service_id)

    except Exception as e:
        logger.exception(f"Error whilst running probe for {postcode}, at {search_distance} "
                         f"miles, for {number_per_type} each of service types: "
                         f"{service_types}")


def snapshot_single_service(service_id, search_role):

    start = time.time()
    service = uec_dos.get_service_by_service_id(service_id, search_role)
    round_trip_time = time.time() - start

    logger.info(f"Ran probe for {service_id} as {search_role} (Took {round_trip_time})")

    if service:
        store_snapshot(service)

        try:
            logger.debug(f"{service_id} - {service['name']}")

            # Only store snapshots and queue status checks if the status has a value
            if service['capacity']['status']['human'] != "":
                logger.debug('Queueing capacity check for {service_id}')

                q.enqueue(has_status_changed,
                          service['id'])
            else:
                logger.debug("Empty capacity - skipping status check")

        except IndexError:
            logger.exception('Service not found')
