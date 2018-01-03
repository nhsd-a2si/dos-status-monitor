from dos_status_monitor import config
from pymongo import MongoClient
import pymongo

from dos_status_monitor import logger

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


def update_status(status):
    query = {'id': status['id']}
    update = {'$set': status}
    r = statuses.update_one(query, update, upsert=True)
    return r


def get_previous_snapshot_for_service(service_id):
    # TODO: Fix so it doesn't throw an error if there's only one previous snapshot
    logger.debug("Getting latest snapshot from database")
    query = {'id': service_id, 'source': config.APP_NAME}
    results = snapshots.find(query).sort([('checkTime',
                                           pymongo.DESCENDING)]).skip(1).limit(1)
    return results


def get_service_watchlist():
    logger.debug("Getting service watchlist from database")
    query = {}
    results = watched_services.find(query).sort([('id',
                                                  pymongo.DESCENDING)])
    return results


def get_service_statuses():
    logger.debug("Getting service status list from database")

    projection = {'_id': False}
    results = statuses.find(projection=projection)\
        .sort([('capacity', pymongo.DESCENDING)])

    result_list = []

    for result in results:
        if result['capacity'] not in ('', 'HIGH'):
            result_list.append(result)

    return result_list


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
