import datetime
import uec_dos
from database import snapshots
import pymongo

from twilio.rest import Client

import config

twilio_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)


def send_sms(to, sms_text):
    message = twilio_client.messages.create(
        to,
        body=sms_text,
        from_="+447403933196")
    
    print(message.sid)
    
    
def has_status_changed(service_id, new_status):
    query = {'id': service_id}
    results = snapshots.find(query).sort([('checkTime', pymongo.DESCENDING)]).limit(1)
    if results.count() > 0:
        for result in results:
            if result['capacity']['status'] == new_status:
                print("No change")
            else:
                print("Changed!")
                data = uec_dos.get_service_by_service_id(service_id)
                updatedBy = data['success']['services'][0]['capacity']['updated']['by']
                status = data['success']['services'][0]['capacity']['status']['human']
                print(updatedBy)
                send_sms(config.MOBILE_NUMBER,
                         f"Capacity changed - {service_id} - {status} by {updatedBy}")
    else:
        print("No previous snapshot available to compare with")


services = uec_dos.get_services('ME13DX', 100, 10)

for service in services:
    print(f"{service['id']} - {service['name']} ({service['odsCode']}) - {service['capacity']['status']['human']}")
    has_status_changed(service['id'], service['capacity']['status']['human'])

    snapshots.insert({'id': service['id'],
                      'checkTime': datetime.datetime.utcnow(),
                      'capacity': {
                      'status': service['capacity']['status']['human'],
                      }})

for record in snapshots.find():
    print(record)
