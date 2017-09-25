import datetime

from twilio.rest import Client

import config
import database
import uec_dos
import utils

sms_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


def send_sms(to, sms_text):
    message = sms_client.messages.create(
        to,
        body=sms_text,
        from_=config.TWILIO_FROM_NUMBER)
    
    print(message.sid)
    
    
def has_status_changed(service_id, new_status):
    
    results = database.get_snapshots_for_service(service_id)
    
    if results.count() > 0:
        
        for result in results:
            
            if result['capacity']['status'] != new_status:
                
                data = uec_dos.get_service_by_service_id(service_id)
                
                service_updated_by = data['success']['services'][0]['capacity']['updated']['by']
                service_status = data['success']['services'][0]['capacity']['status']['human']
                service_rag = data['success']['services'][0]['capacity']['status']['rag']
                service_name = data['success']['services'][0]['name']
                service_postcode = data['success']['services'][0]['postcode']
                service_updated_date = data['success']['services'][0]['capacity']['updated']['date']
                service_updated_time = data['success']['services'][0]['capacity']['updated']['time']
                service_region = data['success']['services'][0]['region']['name']
                
                # Fix the incorrect service_updated_time by subtracting an hour from the supplied time.
                # TODO: Remove this fix when the API is fixed to return the correct local time
                service_updated_time = utils.remove_1_hour_from_time_string(service_updated_time)

                print(f"Status has changed for {service_id} - {service_name} - {service_status} ({service_rag})")
                
                send_sms(config.MOBILE_NUMBER,
                         f"{service_name} ({service_id}) in {service_region} changed to "
                         f"{service_status} ({service_rag}) by {service_updated_by} at {service_updated_time}.")
                
                document = {'id': service_id,
                            'name': service_name,
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


def job():
    
    services = uec_dos.get_services()
    
    print(f"Took snapshot for {len(services)} services")

    for service in services:
        
        has_status_changed(service['id'], service['capacity']['status']['human'])
        
        document = {'id': service['id'],
                    'name': service['name'],
                    'postCode': service['postcode'],
                    'checkTime': datetime.datetime.utcnow(),
                    'capacity': {
                        'status': service['capacity']['status']['human'],
                        'rag': service['capacity']['status']['rag'],
                    },
                    'source': config.APP_NAME}

        database.add_snapshot(document)
