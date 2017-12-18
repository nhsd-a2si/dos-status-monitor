from pymongo import MongoClient
from dos_status_monitor import config
import pymongo

client = MongoClient(config.MONGODB_URI)
db = client.get_database()
snapshots = db['snapshots']
changes = db['changes']

query = {}
results = changes.find(query).sort([('checkTime', pymongo.DESCENDING)])

for result in results:
    print(result)
