import redis
from rq import Worker, Queue, Connection
from dos_status_monitor import config
from raven import Client
from raven.transport.http import HTTPTransport
# from rq.contrib.sentry import register_sentry

client = Client(config.SENTRY_DSN, transport=HTTPTransport)

from dos_status_monitor import config

listen = ["default"]

conn = redis.from_url(config.REDIS_URL)

if __name__ == "__main__":
    with Connection(conn):
        import requests
        import pymongo

        worker = Worker(map(Queue, listen))
        # register_sentry(client, worker)
        worker.work()
