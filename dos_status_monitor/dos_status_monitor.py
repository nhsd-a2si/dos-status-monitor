import datetime
import redis
from rq import Queue

from dos_status_monitor import database, uec_dos, config, slack, logger, sms

# Set up RQ queue
conn = redis.from_url(config.REDIS_URL)
q = Queue(connection=conn)


def update_status(service):

    status = {
        'id': service['id'],
        'name': service['name'],
        'type': service['type']['name'],
        'postCode': service['postcode'],
        'easting': service['easting'],
        'northing': service['northing'],
        'lastUpdated': datetime.datetime.utcnow(),
        'capacity': service['capacity']['status']['human'],
        'rag': service['capacity']['status']['rag'],
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
        'easting': service['easting'],
        'northing': service['northing'],
        'checkTime': datetime.datetime.utcnow(),
        'capacity': {
            'status': service['capacity']['status']['human'],
            'rag': service['capacity']['status']['rag'],
        },
        'source': config.APP_NAME
    }

    database.add_snapshot(snapshot)

    update_status(service)


def has_status_changed(service_id, new_status):
    logger.debug(f'Service ID: {service_id}')
    logger.debug(f'Latest Status: {new_status}')
    results = database.get_previous_snapshot_for_service(service_id)
    if results.count() > 0:
        result = results[0]
        logger.debug(f'Result: {result}')
    else:
        result = None

    if result:

        logger.debug(f'Processing: {result}')

        old_status = result['capacity']['status']
        logger.debug(f'Previous Status: {old_status}')

        if old_status != new_status:

            if (old_status == 'HIGH' and new_status == '') \
                    or (old_status == '' and new_status == 'HIGH'):
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

            # Fix the incorrect service_updated_time by subtracting an hour from the supplied time.
            # TODO: Remove this fix when the API is fixed to return the correct local time
            # service_updated_time = utils.remove_1_hour_from_time_string(service_updated_time)

            logger.info(f"Status has changed for {service_id} - {service_name} - {service_status} ({service_rag})")

            document = {'id': service_id,
                        'name': service_name,
                        'type': service_type,
                        'postCode': service_postcode,
                        'region': service_region,
                        'checkTime': datetime.datetime.utcnow(),
                        'capacity': {
                            'status': service_status,
                            'rag': service_rag,
                            'previousStatus': result['capacity']['status'],
                            'previousRag': result['capacity']['rag'],
                            'updatedBy': service_updated_by,
                            'updatedDate': service_updated_date,
                            'updatedTime': service_updated_time
                        },
                        'source': config.APP_NAME
                        }

            database.add_change(document)
            logger.debug("Change added to database")

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

        else:
            logger.debug(f"Status for {service_id} hasn't changed")


def run_service_search(probe):
    postcode = probe['postcode']
    search_distance = probe['search_distance']
    service_types = probe['service_types']
    number_per_type = probe['number_per_type']

    services = uec_dos.get_services_by_service_search(postcode,
                                                      search_distance,
                                                      service_types,
                                                      number_per_type)

    logger.info(f"Running probe for {postcode}, at {search_distance} "
                f"miles, for {number_per_type} each of service types: "
                f"{service_types} - {len(services)} services")

    for service in services:

        store_snapshot(service)

        if service['capacity']['status']['human'] != "":
            q.enqueue(has_status_changed,
                      service['id'],
                      service['capacity']['status']['human'])
        else:
            logger.debug("Capacity empty - skipping status check")


def check_single_service(service_id):
    service = uec_dos.get_service_by_service_id(service_id)

    try:
        new_capacity = service['capacity']['status']['human']
        logger.debug(service_id)
        logger.debug(service['name'])
        logger.debug(f'New Capacity: {new_capacity}')

        store_snapshot(service)

        if new_capacity != "":
            logger.debug('Capacity not empty - '
                         f'queueing status check for {service_id}')

            q.enqueue(has_status_changed,
                      service['id'],
                      service['capacity']['status']['human'],
                      at_front=True)
        else:
            logger.debug("Capacity is empty so skipping status check")

    except IndexError:
        logger.exception('Service not found')
