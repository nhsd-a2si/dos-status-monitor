# DoS Capacity Status Notifier

## Overview
This is a simple tool which makes use of the DoS REST API.

It allows a 'monitor' to be configured against DoS services, refreshing every X minutes.

If the capacity status of a service changes, a notification will be triggered to a configured Slack channel.

The raw data collected, in order to monitor for changes, is also stored in the form of snapshots.

## Features
See the [Release Notes](RELEASE.md) for more details.

### Watching Services
The tool will allow to types of watch to be configured:

1. A list of specific individual services which will be watched for changes
2. A watch list based on types of service within a particular geographic area (e.g. Emergency Departments within 5 miles of SE1 1LT)

### Notifications
The tool currently supports notifications via SMS or Slack. You can configure one mobile number as an SMS destination, 
and one Slack channel utilising the Slack webhook functionality.

## Technical Details

### Deployment
The app is currently designed to be deployed on a Heroku free tier worker process using a free tier mLab MongoDB database.

### Configuration
There are a number of configuration settings required, which are defined using environment variables.

[Configuration Settings](docs/configuration.md) 

### Security
**NOTE**: By default, the app does not enforce SSL for communications between the application and the database.

When deploying on Heroku with a mLab MongoDB add-on, Heroku ensures that the application and database are deployed 
locally to each other in a way that prevents packet sniffing.

If you were to deploy the application in any other situation, you would need to assess the security of the communications
between the application and database, and take steps appropriate to your deployment scenario.
