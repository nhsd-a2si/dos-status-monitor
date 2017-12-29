import os


def config_string_to_bool(setting):
    if setting.lower() in ('true', 'yes', 'on'):
        return True
    else:
        return False


# Core App Settings
APP_NAME = os.environ.get('APP_NAME', 'DEV')

# Database Settings
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:32771/dos_monitor')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# Scheduling Settings
CHECK_RATE_MINUTES = int(os.environ.get('CHECK_RATE_MINUTES', '5'))
STATUS_UPDATE_RATE_MINUTES = int(os.environ.get('STATUS_UPDATE_RATE_MINUTES', '60'))

# UEC DoS Settings
UEC_DOS_USERNAME = os.environ.get('UEC_DOS_USERNAME')
UEC_DOS_PASSWORD = os.environ.get('UEC_DOS_PASSWORD')
UEC_DOS_BASE_URL = os.environ.get('UEC_DOS_BASE_URL')

# Slack Notification Settings
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#random')
SLACK_ENABLED = config_string_to_bool(os.environ.get('SLACK_ENABLED', ''))

# SMS Notification Settings
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = os.environ.get('TWILIO_FROM_NUMBER')
MOBILE_NUMBER = os.environ.get('MOBILE_NUMBER')
SMS_ENABLED = config_string_to_bool(os.environ.get('SMS_ENABLED', ''))

# Monitor Settings
# e.g. "POSTCODE:DISTANCE:TYPES:NUMBER|POSTCODE:DIST:TYPES:NUMBER"
PROBE_LIST = os.environ.get('PROBE_LIST', '')
