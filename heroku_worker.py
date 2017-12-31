import redis
import rollbar
from rq import Worker, Queue, Connection

from dos_status_monitor import config

rollbar.init(config.ROLLBAR_ACCESS_TOKEN, config.APP_NAME)

listen = ['default']

conn = redis.from_url(config.REDIS_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))

        try:
            worker.work()

        except:
            rollbar.report_exc_info()
