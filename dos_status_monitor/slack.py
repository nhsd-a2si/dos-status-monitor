import requests
import json
import time
from dos_status_monitor import config, database, logger

url = config.SLACK_WEBHOOK_URL
slack_channel = config.SLACK_CHANNEL
app_name = config.APP_NAME

emojis = {
    'HIGH': ':green_heart:',
    'LOW': ':large_orange_diamond:',
    'NONE': ':red_circle:'
}


def send_slack_notification(service_name, region,
                            capacity, old_status,
                            service_type, changed_at, 
                            changed_by):

    automatic_change = True if changed_by == 'ROBOT' else False

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
        
    if automatic_change:
        description = f"{service_name} Status cleared by the :robot_face:"
    else:
        description = f"{service_name} was changed to {emoji} {capacity}"

    message = {
                "username": f"Capacity Monitor ({app_name})",
                "channel": slack_channel,
                "attachments": [
                   {
                        "fallback": description,
                        "pretext": description,
                        "fields": [
                            {
                                "title": f"Previously",
                                "value": f"{old_status}",
                                "short": True
                            },
                            {
                                "title": "Region",
                                "value": f"{region}",
                                "short": True
                            },
                            {
                                "title": "Changed At",
                                "value": f"{changed_at}",
                                "short": True
                            },
                            {
                                "title": "Type Of Service",
                                "value": f"{service_type}",
                                "short": True
                            }
                        ]
                   }
                ]
            }

    if not automatic_change:
        message['attachments'][0]['color'] = f"{severity}"

    body = json.dumps(message)
    
    logger.info(f'Sending Slack notification to '
                f'{config.SLACK_CHANNEL}')

    r = requests.post(url, body)

    if r.status_code == 200:
        return True


def send_slack_status_update():

    service_list = database.get_low_statuses()

    now = time.strftime("%H:%M")

    if len(service_list) < 1:
        message_text = f"At {now}, there are no services indicating " \
                       f"low capacity."
    else:
        message_text = f"At {now}, these services are indicating low " \
                       f"capacity (a status of NONE means they are not " \
                       f"returning in DoS searches)."

    message = {
        "username": f"Capacity Monitor ({app_name})",
        "channel": slack_channel,
        "attachments": [
            {
                "fallback": "Capacity Status Summary",
                "pretext": message_text
            }
        ]
    }

    fields = []

    for service in service_list:

        capacity = service['capacity']
        name = service['name']

        field = {
            "title": name,
            "value": f"{emojis[capacity]}{capacity}",
            "short": True
        }

        fields.append(field)

    message['attachments'][0]['fields'] = fields

    body = json.dumps(message)

    r = requests.post(url, body)

    if r.status_code == 200:
        return True
