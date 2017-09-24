import config
import database
import datetime
from twilio.rest import Client
import uec_dos

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
                
                print("Status has changed!")
                
                data = uec_dos.get_service_by_service_id(service_id)
                
                service_updated_by = data['success']['services'][0]['capacity']['updated']['by']
                service_status = data['success']['services'][0]['capacity']['status']['human']
                service_rag = data['success']['services'][0]['capacity']['status']['rag']
                service_name = data['success']['services'][0]['name']
                service_postcode = data['success']['services'][0]['postcode']
                service_updated_date = data['success']['services'][0]['capacity']['updated']['date']
                service_updated_time = data['success']['services'][0]['capacity']['updated']['time']
                
                send_sms(config.MOBILE_NUMBER,
                         f"Capacity changed for {service_name} ({service_id}). \n"
                         f"It was changed to {service_status} by {service_updated_by}.")
                
                document = {'id': service_id,
                            'name': service_name,
                            'postCode': service_postcode,
                            'checkTime': datetime.datetime.utcnow(),
                            'status': service_status,
                            'rag': service_rag,
                            'previousStatus': result['capacity']['status'],
                            'previousRag': result['capacity']['rag'],
                            'updatedBy': service_updated_by,
                            'updatedDate': service_updated_date,
                            'updatedTime': service_updated_time
                            }
            
                database.add_change(document)
                return
    
    else:
    
        print("No previous snapshot available to compare with")
        return


def job():
    
    services = uec_dos.get_services()

    for service in services:
        
        print(f"{service['id']} - {service['name']} ({service['odsCode']}) - {service['capacity']['status']['human']}")

        has_status_changed(service['id'], service['capacity']['status']['human'])
        
        document = {'id': service['id'],
                    'name': service['name'],
                    'postCode': service['postcode'],
                    'checkTime': datetime.datetime.utcnow(),
                    'capacity': {
                        'status': service['capacity']['status']['human'],
                        'rag': service['capacity']['status']['rag'],
                    }}

        database.add_snapshot(document)
    

