from dos_status_monitor import config
from pymongo import MongoClient
import pymongo
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DSM')

client = MongoClient(config.MONGODB_URI)
db = client.get_database()

# Set up collections
snapshots = db['snapshots']
changes = db['changes']
statuses = db['statuses']
watched_services = db['watched_services']


def add_change(document):
    changes.insert(document)


def add_snapshot(document):
    snapshots.insert(document)


def get_snapshots_for_service(service_id):
    logger.debug("Getting latest snapshot from database")
    query = {'id': service_id}
    results = snapshots.find(query).sort([('checkTime',
                                           pymongo.DESCENDING)]).skip(1).limit(1)
    return results


def get_service_watchlist():
    logger.debug("Getting service watchlist from database")
    query = {}
    results = watched_services.find(query).sort([('id',
                                                  pymongo.DESCENDING)])
    return results


def add_watched_service(service_id):
    logger.debug(f'Adding watch for service {service_id}')
    query = {'id': service_id}
    update = {'id': service_id}
    r = watched_services.update(query, update, upsert=True)
    return r


def remove_watched_service(service_id):
    logger.debug(f'Removing watch for service {service_id}')
    query = {'id': service_id}
    r = watched_services.delete_many(query)
    return r
