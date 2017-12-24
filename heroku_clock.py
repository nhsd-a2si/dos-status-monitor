import schedule
import time
import redis
from rq import Queue

from dos_status_monitor import dos_status_monitor, probes, config, slack

# Set up RQ queue
conn = redis.from_url(config.REDIS_URL)
q = Queue(connection=conn)


def add_search_job():
    probe_list = probes.get_probe_list()
    
    for probe in probe_list:
        print("Adding job to queue")
        q.enqueue(dos_status_monitor.run_search,
                  probe,
                  ttl=f'{config.CHECK_RATE_MINUTES}m')


def add_service_jobs():
    service_list = probes.get_watched_service_list()
    print(f'Watched Services: {service_list.count()}')
    for service in service_list:
        service_id = service['id']
        print(f"Adding job for {service_id}")
        q.enqueue(dos_status_monitor.check_single_service,
                  service_id,
                  ttl=f'{config.CHECK_RATE_MINUTES}m')


def add_service_status_job():
    print('Queueing Slack status update')
    q.enqueue(slack.send_slack_status_update,
              ttl=f'{config.STATUS_UPDATE_RATE_MINUTES}m')


add_search_job()
add_service_jobs()
add_service_status_job()

schedule.every(config.CHECK_RATE_MINUTES).minutes.do(add_search_job)
schedule.every(config.CHECK_RATE_MINUTES).minutes.do(add_service_jobs)
schedule.every(config.STATUS_UPDATE_RATE_MINUTES).minutes.do(add_service_status_job)

print(f"{len(probes.get_probe_list())} probes configured to run "
      f"every {config.CHECK_RATE_MINUTES} minute(s).")

print("Slack Status Summary will run every "
      f"{config.STATUS_UPDATE_RATE_MINUTES} minute(s).")

while True:
    print(f"Ping!")
    schedule.run_pending()
    time.sleep(60)
