import datetime
import redis
from rq import Queue

from twilio.rest import Client

from dos_status_monitor import database, uec_dos, config, slack, logger

sms_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

# Set up RQ queue
conn = redis.from_url(config.REDIS_URL)
q = Queue(connection=conn)


def send_sms(to, sms_text):

    logger.info("Sending SMS")

    message = sms_client.messages.create(
        to,
        body=sms_text,
        from_=config.TWILIO_FROM_NUMBER)

    logger.debug(message.sid)


def store_snapshot(service):
    if service['capacity']['status']['human']:
        print(f"{service['name']} - {service['capacity']['status']['human']}")

    snapshot = {
        'id': service['id'],
        'name': service['name'],
        'type': service['type']['name'],
        'postCode': service['postcode'],
        'checkTime': datetime.datetime.utcnow(),
        'capacity': {
            'status': service['capacity']['status']['human'],
            'rag': service['capacity']['status']['rag'],
        },
        'source': config.APP_NAME
    }

    database.add_snapshot(snapshot)

    status = {
        'id': service['id'],
        'name': service['name'],
        'type': service['type']['name'],
        'postCode': service['postcode'],
        'checkTime': datetime.datetime.utcnow(),
        'capacity': service['capacity']['status']['human'],
        'rag': service['capacity']['status']['rag'],
        'source': config.APP_NAME
    }

    r = database.add_status(status)
    logger.debug(r)


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
                logger.info("Skipping change as it's just the 24h robot")
                return

            data = uec_dos.get_service_by_service_id(service_id)

            service_updated_by = data['success']['services'][0]['capacity']['updated']['by']
            service_status = data['success']['services'][0]['capacity']['status']['human']
            service_rag = data['success']['services'][0]['capacity']['status']['rag']
            service_name = data['success']['services'][0]['name']
            service_postcode = data['success']['services'][0]['postcode']
            service_updated_date = data['success']['services'][0]['capacity']['updated']['date']
            service_updated_time = data['success']['services'][0]['capacity']['updated']['time']
            service_region = data['success']['services'][0]['region']['name']
            service_type = data['success']['services'][0]['type']['name']

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

            q.enqueue(send_sms, config.MOBILE_NUMBER,
                      f"{service_name} ({service_id}) in {service_region} changed to "
                      f"{service_status} ({service_rag}) by {service_updated_by} at {service_updated_time}.")

            q.enqueue(slack.send_slack_notification,
                      service_name,
                      service_region,
                      service_status,
                      old_status,
                      service_type,
                      service_updated_time)

            logger.debug("Change added to database")

        else:
            logger.debug("Status hasn't changed")


def run_search(probe):
    postcode = probe['postcode']
    search_distance = probe['search_distance']
    service_types = probe['service_types']
    number_per_type = probe['number_per_type']

    logger.info(f"Running probe for {postcode}, at {search_distance} miles, "
                f"for {number_per_type} each of service types: {service_types}")

    services = uec_dos.get_services(postcode, search_distance, service_types, number_per_type)

    logger.info(f"Took snapshot for {len(services)} services")

    for service in services:

        store_snapshot(service)

        if service['capacity']['status']['human'] != "":
            q.enqueue(has_status_changed,
                      service['id'],
                      service['capacity']['status']['human'])
        else:
            logger.debug("Capacity is empty so skipping status check")


def check_single_service(service_id):
    data = uec_dos.get_service_by_service_id(service_id)
    service = data['success']['services'][0]
    new_capacity = service['capacity']['status']['human']
    logger.debug(service_id)
    logger.debug(service['name'])
    logger.debug(f'New Capacity: {new_capacity}')

    store_snapshot(service)

    if new_capacity != "":
        logger.debug('Capacity is set, so queueing for a status check')
        q.enqueue(has_status_changed,
                  service['id'],
                  service['capacity']['status']['human'])
    else:
        logger.debug("Capacity is empty so skipping status check")
