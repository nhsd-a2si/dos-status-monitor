import redis
from rq import Worker, Queue, Connection

from dos_status_monitor import config

listen = ["default"]

conn = redis.from_url(config.REDIS_URL)

if __name__ == "__main__":
    with Connection(conn):
        import requests
        import pymongo

        worker = Worker(map(Queue, listen))
        worker.work()
