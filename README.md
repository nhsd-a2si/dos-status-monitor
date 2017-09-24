# DoS Capacity Status Notifier

## About
This is a simple tool which makes use of the DoS REST API.

It allows a 'watch' to be configured against DoS services, refreshing every 10 minutes.

If the capacity status of a service changes,  
a notification will be triggered.

## Features

### Watching Services
The tool will allow to types of watch to be configured:

1. A list of specific individual services which will be watched for changes
2. A watch list based on types of service within a particular geographic area (e.g. Emergency Departments within 5 miles of SE1 1LT)

### Notifications
The tool will initially support notification by SMS only.

## Technical Details

### Deployment
The app is currently designed to be deployed on a Heroku free tier worker process using a free tier MongoDB database.

### Configuration
There are a number of configuration settings required, which are defined as environment variables:

#### Core App Settings
MONGODB_URI - Should contain a full MongoDB connection string e.g. `mongodb://localhost:32707/database`
CHECK_RATE_MINUTES - The number of minutes between each status check

#### UEC DoS Settings
UEC_DOS_USERNAME - The username to use when connecting to the DoS REST API  
UEC_DOS_PASSWORD - The password to use when connecting to the DoS REST API
UEC_DOS_BASE_URL - The base URL to use for the DoS REST API (e.g. https://uat.dos.nhs.uk)
UEC_DOS_POSTCODE - The postcode from which the search should be performed
UEC_DOS_SERVICE_TYPES - A list of service type codes to define the services that should be monitored (e.g. 40,45,46)  

#### SMS Settings
TWILIO_ACCOUNT_SID - The Account SID for sending SMS via Twilio  
TWILIO_AUTH_TOKEN - The auth token for sending SMS via Twilio
MOBILE_NUMBER - The mobile number that should receive the SMS notifications

#### Email Settings (Not yet implemented)
SENDGRID_API_KEY - The API key to be used when sending emails via Sendgrid  