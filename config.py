import os

UEC_DOS_USERNAME = os.environ.get('UEC_DOS_USERNAME')
UEC_DOS_PASSWORD = os.environ.get('UEC_DOS_PASSWORD')
TWILIO_ACCOUNT_SID= os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.environ.get('TWILIO_AUTH_TOKEN')
MONGODB_URI= os.environ.get('MONGODB_URI')
MOBILE_NUMBER = os.environ.get('MOBILE_NUMBER')
CHECK_RATE_MINUTES = int(os.environ.get('CHECK_RATE_MINUTES', '5'))
