from dos_status_monitor import config
from pymongo import MongoClient
from datetime import datetime
from datetime import date

from dos_status_monitor import logger

client = MongoClient(config.MONGODB_URI)
db = client.get_database()

# Set up collections
snapshots = db["snapshots"]


# Get week's worth of snapshots
def delete_old_snapshots():
    logger.debug(f"Deleting old snapshots")
    query = {
        "snapshotTime": {"$lt": datetime.combine(date.today(), datetime.min.time())}
    }
    count = snapshots.count_documents(filter=query)
    results = snapshots.delete_many(filter=query)
    print(f"Counted {count}. Deleted {results.deleted_count}")
