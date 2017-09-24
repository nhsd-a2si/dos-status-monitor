import config
from pymongo import MongoClient

client = MongoClient(config.MONGODB_URI)
db = client.get_database()
snapshots = db['snapshots']
