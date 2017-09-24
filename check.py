import config
from database import snapshots, add_change
import datetime
import pymongo
from twilio.rest import Client
import uec_dos

twilio_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


def send_sms(to, sms_text):
    message = twilio_client.messages.create(
        to,
        body=sms_text,
        from_=config.TWILIO_FROM_NUMBER)
    
    print(message.sid)
    
    
def has_status_changed(service_id, new_status):
    query = {'id': service_id}
    results = snapshots.find(query).sort([('checkTime', pymongo.DESCENDING)]).limit(1)
    if results.count() > 0:
        for result in results:
            if result['capacity']['status'] != new_status:
                print("Status has changed!")
                data = uec_dos.get_service_by_service_id(service_id)
                service_updatedBy = data['success']['services'][0]['capacity']['updated']['by']
                service_status = data['success']['services'][0]['capacity']['status']['human']
                service_name = data['success']['services'][0]['name']
                service_updated_date = data['success']['services'][0]['capacity']['updated']['date']
                service_updated_time = data['success']['services'][0]['capacity']['updated']['time']
                
                send_sms(config.MOBILE_NUMBER,
                         f"Capacity changed for {service_name} ({service_id}). \n"
                         f"It was changed to {service_status} by {service_updatedBy}.")
                
                document = {'id': service_id,
                            'name': service_name,
                            'checkTime': datetime.datetime.utcnow(),
                            'status': service_status,
                            'previousStatus': result['capacity']['status'],
                            'updatedBy': service_updatedBy,
                            'updatedDate': service_updated_date,
                            'updatedTime': service_updated_time
                            }
            
                add_change(document)
    else:
        print("No previous snapshot available to compare with")


def job():
    services = uec_dos.get_services()

    for service in services:
        print(f"{service['id']} - {service['name']} ({service['odsCode']}) - {service['capacity']['status']['human']}")
        has_status_changed(service['id'], service['capacity']['status']['human'])
    
        snapshots.insert({'id': service['id'],
                          'checkTime': datetime.datetime.utcnow(),
                          'capacity': {
                          'status': service['capacity']['status']['human'],
                          }})