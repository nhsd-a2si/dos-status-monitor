import requests
import json
from dos_status_monitor import config

url = config.SLACK_WEBHOOK_URL


def send_slack_notification(service_name, region, capacity, changed_at):
    if capacity == 'HIGH':
        severity = 'ok'
        rag_colour = 'GREEN'
    elif capacity == 'LOW':
        severity = 'warning'
        rag_colour = 'AMBER'
    elif capacity == 'NONE':
        severity = 'danger'
        rag_colour = 'RED'
    message = {
                "username": "DoS Status Monitor",
                "channel": "#capacity_demand",
                "attachments": [
                   {
                        "fallback": f"{rag_colour}: {service_name}",
                        "pretext": f"{service_name} has changed to {rag_colour}",
                        "color": f"{severity}",
                        "fields": [
                           {
                               "title": "Region",
                               "value": f"{region}"
                           },
                           {
                              "title": "Status",
                              "value": f"{rag_colour}"
                           },
                           {
                               "title": "Capacity",
                               "value": f"{capacity}"
                           },
                           {
                              "title": "Changed At",
                              "value": f"{changed_at}"
                           }
                        ]
                   }
                ]
            }

    body = json.dumps(message)

    r = requests.post(url, body)

    if r.status_code == 200:
        return True
