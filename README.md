# DoS Capacity Status Notifier

## Overview
This is a simple tool which makes use of the DoS REST API.

It allows a 'monitor' to be configured against DoS services, refreshing every X minutes.

If the capacity status of a service changes, a notification will be triggered.

## Features
See the [Release Notes](RELEASE.md) for more details.

### Watching Services
The tool will allow to types of watch to be configured:

1. A list of specific individual services which will be watched for changes
2. A watch list based on types of service within a particular geographic area (e.g. Emergency Departments within 5 miles of SE1 1LT)

### Notifications
The tool will initially support notification by SMS only.

## Technical Details

### Deployment
The app is currently designed to be deployed on a Heroku free tier worker process using a free tier mLab MongoDB database.

### Configuration
There are a number of configuration settings required, which are defined as environment variables:

### Security
**NOTE**: By default, the app does not enforce SSL for communications between the application and the database.

When deploying on Heroku with a mLab MongoDB add-on, Heroku ensures that the application and database are deployed 
locally to each other in a way that prevents packet sniffing.

If you were to deploy the application in any other situation, you would need to assess the security of the communications
between the application and database, and take steps appropriate to your deployment scenario.


#### Core App Settings
MONGODB_URI - Should contain a full MongoDB connection string e.g. `mongodb://localhost:32707/database`  
CHECK_RATE_MINUTES - The number of minutes between each status check  

#### UEC DoS Settings
UEC_DOS_USERNAME - The username to use when connecting to the DoS REST API  
UEC_DOS_PASSWORD - The password to use when connecting to the DoS REST API  
UEC_DOS_BASE_URL - The base URL to use for the DoS REST API (e.g. https://uat.dos.nhs.uk)  
UEC_DOS_POSTCODE - The postcode from which the search should be performed  
UEC_DOS_SERVICE_TYPES - A list of service type codes to define the services that should be monitored (e.g. 40,45,46)
UEC_DOS_SEARCH_DISTANCE - The distance from the postcode to search within (Default: 100 miles)
UEC_DOS_NUMBER_PER_TYPE - The number of services to return for each type in the list of service types (Default: 10)

#### SMS Settings
TWILIO_ACCOUNT_SID - The Account SID for sending SMS via Twilio    
TWILIO_AUTH_TOKEN - The auth token for sending SMS via Twilio  
TWILIO_FROM_NUMBER - The number from which Twilio SMS will be sent    
MOBILE_NUMBER - The mobile number that should receive the SMS notifications  

#### Email Settings (Not yet implemented)
SENDGRID_API_KEY - The API key to be used when sending emails via Sendgrid    
