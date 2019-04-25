from dos_status_monitor import config
from pymongo import MongoClient
from datetime import datetime
import pprint

from dos_status_monitor import logger

client = MongoClient(config.MONGODB_URI)
db = client.get_database()

# Set up collections
snapshots = db['snapshots']


# Get week's worth of snapshots
def get_old_snapshots():
    logger.debug(f"Getting previous snapshots")
    query = {"snapshotTime": {"$lt": datetime.now()}}
    results = snapshots.find(query).limit(1)
    try:
        for result in results:
            pprint.pprint(result)

    except TypeError:
        logger.debug(f'No snapshots found')
        return None

# TODO: Save snapshots to temporary CSV

# TODO: Upload CSV to S3

# TODO: Delete exported snapshots
