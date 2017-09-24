# DoS Capacity Notification Tool

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

## Deployment
The app is designed to be deployed on Heroku.

### Configuration
There are a number of environment variables required:

MONGODB_URI - Should contain a full MongoDB connection string e.g. `mongodb://localhost:32707/database`  
UEC_DOS_USERNAME - The username to use when connecting to the DoS REST API  
UEC_DOS_PASSWORD - The password to use when connecting to the DoS REST API  
TWILIO_ACCOUNT_SID - The Account SID for sending SMS via Twilio  
TWILIO_AUTH_TOKEN - The auth token for sending SMS via Twilio  