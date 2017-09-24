import os

# Core App Settings
MONGODB_URI = os.environ.get('MONGODB_URI')
CHECK_RATE_MINUTES = int(os.environ.get('CHECK_RATE_MINUTES', '5'))

# UEC DoS Settings
UEC_DOS_USERNAME = os.environ.get('UEC_DOS_USERNAME')
UEC_DOS_PASSWORD = os.environ.get('UEC_DOS_PASSWORD')
UEC_DOS_BASE_URL = os.environ.get('UEC_DOS_BASE_URL')
UEC_DOS_POSTCODE = os.environ.get('UEC_DOS_POSTCODE')
UEC_DOS_SERVICE_TYPES = os.environ.get('UEC_DOS_SERVICE_TYPES')

# SMS Settings
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
MOBILE_NUMBER = os.environ.get('MOBILE_NUMBER')

# Email Settings
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
