from dos_status_monitor import config
from pymongo import MongoClient, errors
import pymongo

from dos_status_monitor import logger

client = MongoClient(config.MONGODB_URI)
db = client.get_database()

# Set up collections
snapshots = db['snapshots']
changes = db['changes']
statuses = db['statuses']
watched_services = db['watched_services']
watched_searches = db['watched_searches']


def add_change(document):
    changes.insert(document)
    logger.debug(f"Added change event for {document['id']}")


def add_snapshot(document):
    try:
        snapshots.insert(document)
        logger.debug(f"Added snapshot for {document['id']}")
    except errors.WriteError:
        logger.error("Unable to write snapshot to database")


def update_status(document):
    query = {'id': document['id']}
    update = {'$set': document}
    try:
        r = statuses.update_one(query, update, upsert=True)
        logger.debug(f"Updated status for {document['id']}")
        return r
    except:
        logger.error(f"Failed to update status for {document['id']}")
        raise


def get_most_recent_snapshot_for_service(service_id):
    # TODO: Fix so it doesn't throw an error if there's only one previous snapshot
    logger.debug("Getting latest snapshot from database")
    query = {'id': service_id, 'source': config.APP_NAME}
    results = snapshots.find(query).sort([('snapshotTime', pymongo.DESCENDING)]).limit(1)
    result = results[0]
    return result


def get_watched_services():
    logger.debug("Getting service watchlist from database")
    query = {}
    results = watched_services.find(query)
    return results


def get_watched_searches():
    logger.debug("Getting search watchlist from database")
    query = {}
    results = watched_searches.find(query)
    return list(results)


def get_all_statuses():
    logger.debug("Getting all service statuses")

    projection = {'_id': False}
    results = statuses.find(projection=projection)\
        .sort([('capacity', pymongo.DESCENDING)])

    result_list = [result for result in results
                   if result['capacity'] != ""]

    return result_list


def get_all_postcodes():
    logger.debug("Getting all service postcodes")

    projection = {'_id': False}
    results = statuses.find(projection=projection)

    result_list = [result for result in results]

    return result_list


def get_low_statuses():
    logger.debug("Getting low service statuses")

    projection = {'_id': False}
    results = statuses.find(projection=projection)\
        .sort([('capacity', pymongo.DESCENDING)])

    result_list = [result for result in results
                   if result['capacity'] not in ('', 'HIGH')]

    return result_list


def get_status_for_single_service(service_id):
    logger.debug(f"Getting status for single service {service_id}")
    query = {'id': service_id}
    projection = {'id': True, 'capacity': True, 'rag': True}
    result = statuses.find_one(query, projection=projection)
    try:
        return result

    except TypeError:
        logger.debug(f'No status found for {service_id}')
        return None


def add_watched_service(service_id):
    logger.debug(f'Adding watch for service {service_id}')
    query = {'id': service_id}
    update = {'id': service_id}
    r = watched_services.replace_one(query, update, upsert=True)
    return r


def remove_watched_service(service_id):
    logger.debug(f'Removing watch for service {service_id}')
    query = {'id': service_id}
    r = watched_services.delete_many(query)
    return r
