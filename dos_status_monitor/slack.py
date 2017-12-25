import requests
import json
import time
from dos_status_monitor import config, database

url = config.SLACK_WEBHOOK_URL
slack_channel = config.SLACK_CHANNEL
app_name = config.APP_NAME


def send_slack_notification(service_name, region,
                            capacity, old_status,
                            service_type, changed_at):
    if capacity == 'HIGH':
        severity = 'good'
        rag_colour = 'GREEN'
        emoji = ':green_heart:'
    elif capacity == 'LOW':
        severity = 'warning'
        rag_colour = 'AMBER'
        emoji = ':large_orange_diamond:'
    elif capacity == 'NONE':
        severity = 'danger'
        rag_colour = 'RED'
        emoji = ':red_circle:'

    if old_status == 'HIGH':
        old_severity = 'good'
        old_rag_colour = 'GREEN'
        old_emoji = ':green_heart:'
    elif old_status == 'LOW':
        old_severity = 'warning'
        old_rag_colour = 'AMBER'
        old_emoji = ':large_orange_diamond:'
    elif old_status == 'NONE':
        old_severity = 'danger'
        old_rag_colour = 'RED'
        old_emoji = ':red_circle:'

    message = {
                "username": f"Capacity Monitor ({app_name})",
                "channel": slack_channel,
                "attachments": [
                   {
                        "fallback": f"{service_name} has changed to {capacity} - {rag_colour}",
                        "pretext": f"{service_name} has changed to {emoji} {capacity}",
                        "color": f"{severity}",
                        "fields": [
                            {
                                "title": f"Previously",
                                "value": f"{old_status}",
                                "short": True
                            },
                            {
                                "title": ":world_map:",
                                "value": f"{region}",
                                "short": True
                            },
                            {
                                "title": ":mantelpiece_clock:",
                                "value": f"{changed_at}",
                                "short": True
                            },
                            {
                                "title": ":hospital:",
                                "value": f"{service_type}",
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
