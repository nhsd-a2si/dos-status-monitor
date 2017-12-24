from dos_status_monitor import config
from pymongo import MongoClient
import pymongo
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('DSM')

client = MongoClient(config.MONGODB_URI)
db = client.get_database()
snapshots = db['snapshots']
changes = db['changes']


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
