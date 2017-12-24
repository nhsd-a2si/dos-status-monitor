import requests
import json
import time
from dos_status_monitor import config, database

url = config.SLACK_WEBHOOK_URL
slack_channel = config.SLACK_CHANNEL
app_name = config.APP_NAME


def send_slack_notification(service_name, region, capacity, changed_at):
    if capacity == 'HIGH':
        severity = 'good'
        rag_colour = 'GREEN'
    elif capacity == 'LOW':
        severity = 'warning'
        rag_colour = 'AMBER'
    elif capacity == 'NONE':
        severity = 'danger'
        rag_colour = 'RED'

    message = {
                "username": f"Capacity Monitor ({app_name})",
                "channel": slack_channel,
                "attachments": [
                   {
                        "fallback": f"{rag_colour}: {service_name}",
                        "pretext": f"*{service_name}* has changed to *{rag_colour}*",
                        "color": f"{severity}",
                        "fields": [
                           {
                               "title": "Region",
                               "value": f"{region}",
                               "short": True
                           },
                           {
                               "title": "Status",
                               "value": f"{rag_colour}",
                               "short": True
                           },
                           {
                               "title": "Capacity",
                               "value": f"{capacity}",
                               "short": True
                           },
                           {
                               "title": "Changed At",
                               "value": f"{changed_at}",
                               "short": True
                           }
                        ]
                   }
                ]
            }

    body = json.dumps(message)

    r = requests.post(url, body)

    if r.status_code == 200:
        return True


def send_slack_status_update():

    service_list = database.get_service_statuses()

    now = time.strftime("%H:%M")

    message = {
        "username": f"Capacity Monitor ({app_name})",
        "channel": slack_channel,
        "attachments": [
            {
                "fallback": "Capacity Status Summary",
                "pretext": f"At {now}, these services are indicating low capacity  "
                           "(status of NONE means they are not returning in DoS searches)."
            }
        ]
    }

    fields = []

    for service in service_list:

        capacity = service['capacity']
        name = service['name']

        field = {
            "title": name,
            "value": capacity,
            "short": True
        }

        fields.append(field)

    message['attachments'][0]['fields'] = fields

    body = json.dumps(message)

    r = requests.post(url, body)

    if r.status_code == 200:
        return True
