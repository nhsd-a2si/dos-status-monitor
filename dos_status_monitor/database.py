from dos_status_monitor import config
from pymongo import MongoClient
import pymongo

client = MongoClient(config.MONGODB_URI)
db = client.get_database()
snapshots = db['snapshots']
changes = db['changes']


def add_change(document):
    changes.insert(document)


def add_snapshot(document):
    snapshots.insert(document)


def get_snapshots_for_service(service_id):
    query = {'id': service_id}
    results = snapshots.find(query).sort([('checkTime', pymongo.DESCENDING)]).limit(1)
    return results
