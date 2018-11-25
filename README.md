# DoS Capacity Status Notifier v0.3

## Overview
This is a simple tool which makes use of the DoS REST API.

It allows a 'monitor' to be configured against DoS services, refreshing every X minutes. It is also possible to configur a monitor against broader searches, effectively monitoring any service returned by those searches.

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

### Snapshots
A snapshot of service information is taken for every monitored service at the refresh rate specified in configuration.

Monitored services will be any service that is specifically monitored (watched_services collection) and also any services returned from the monitored searches (watched_searches collection).

*Note: The snapshot information can grow quite quickly, and there is currently no automated method for clearing this out. To ensure the database instance does not reach capacity, you will need to manually export any snapshot data you wish to keep and clear those documents out of the collection.*

## Technical Details

### Deployment
The app is currently designed to be deployed on a Heroku free tier worker process using a free tier mLab MongoDB database.

### Configuration
There are a number of configuration settings required, which are defined using environment variables.

[Configuration Settings](docs/configuration.md)

### Database
The app uses MongoDB to store snapshot and change information. The search configurations are also stored in collections in the database.

### Security
MongoDB doesn't always enforce SSL connections by default, however the app is currently backed off against Atlas (MongoDB Cloud Cluster) which does enforce SSL between the app and the database.

If deploying against a different MongoDB instance, you must ensure that the appropriate level of security is in place for the comms between the app and the database.
