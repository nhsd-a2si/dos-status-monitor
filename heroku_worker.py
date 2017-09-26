import redis
from rq import Worker, Queue, Connection

import config

listen = ['default']

conn = redis.from_url(config.REDIS_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()