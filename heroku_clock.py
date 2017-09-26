import schedule
import time
import redis
from rq import Queue

import check
import config
import datetime

print(f"Checking for types {config.UEC_DOS_SERVICE_TYPES} every {config.CHECK_RATE_MINUTES} minute(s)")

# Set up RQ queue
listen = ['default']
conn = redis.from_url(config.REDIS_URL)
q = Queue(connection=conn)


def add_job():
    print("Adding check job to queue")
    q.enqueue(check.job,
              ttl=f'{config.CHECK_RATE_MINUTES}m')


schedule.every(config.CHECK_RATE_MINUTES).minutes.do(add_job)

add_job()

while True:
    print(f"Ping!")
    schedule.run_pending()
    time.sleep(60)
