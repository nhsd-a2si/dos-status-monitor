import config
from pymongo import MongoClient

client = MongoClient(config.MONGODB_URI)
db = client.get_database()
snapshots = db['snapshots']
changes = db['changes']


def add_change(document):
    changes.insert(document)
