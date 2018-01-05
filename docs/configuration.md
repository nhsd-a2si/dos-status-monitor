# Configuration Settings

#### Core App Settings
APP_NAME - A short name for the instance of the app (will be used in logs, database etc.)

#### Scheduling Settings
CHECK_RATE_MINUTES - The number of minutes between each service status check
STATUS_UPDATE_RATE_MINUTES - The number of minutes between Slack Status updates

#### Database Settings
MONGODB_URI - A connection URL for (e.g. `mongodb://username:password@localhost:32707/database`)  
REDIS_URL - A connection URI for Redis instance to be used for job queue (e.g. `redis://username:password@localhost:6379`)

#### UEC DoS API Settings
UEC_DOS_USERNAME - The username to use when connecting to the DoS REST API  
UEC_DOS_PASSWORD - The password to use when connecting to the DoS REST API  
UEC_DOS_BASE_URL - The base URL to use for the DoS REST API (e.g. https://uat.dos.nhs.uk)  

#### SMS Settings
TWILIO_ACCOUNT_SID - The Account SID for sending SMS via Twilio    
TWILIO_AUTH_TOKEN - The auth token for sending SMS via Twilio  
TWILIO_FROM_NUMBER - The number from which Twilio SMS will be sent    
MOBILE_NUMBER - The mobile number that should receive the SMS notifications
SMS_ENABLED - Enable / Disable SMS notifications

#### Slack Settings# Slack Notification Settings
SLACK_WEBHOOK_URL - The URL for the Slack Incoming Webhook (obtained from Slack admin)
SLACK_CHANNEL - The channel that you would like notifications to be sent to (e.g. #capacity-updates)
SLACK_ENABLED - Enable / Disable Slack notifications
  
#### Search Settings
PROBE_LIST - A list of searches to perform every X minutes to retrieve service snapshots.    
*Note: The search configuration will be moved to the database eventually*

#### Basic Auth Settings (for API endpoints)
BASIC_AUTH_USERNAME - Username for Basic Auth
BASIC_AUTH_PASSWORD - Password for Basic Auth
BASIC_AUTH_FORCE - Set to True to force basic auth for all endpoints (default: True)