import schedule
import time
import redis
import rollbar
from rq import Queue

from dos_status_monitor import dos_status_monitor, probes, config, slack

rollbar.init(config.ROLLBAR_ACCESS_TOKEN, config.APP_NAME)

# Set up RQ queue
conn = redis.from_url(config.REDIS_URL)
q = Queue(connection=conn)


def add_search_jobs():
    probe_list = probes.get_probe_list()
    search_job_count = 0
    
    for probe in probe_list:
        q.enqueue(dos_status_monitor.run_service_search,
                  probe,
                  ttl=f'{config.CHECK_RATE_MINUTES}m')
        search_job_count += 1

    print(f'Added {search_job_count} search jobs to the queue')


def add_service_jobs():
    service_list = probes.get_watched_service_list()
    service_job_count = 0

    for service in service_list:
        service_id = service['id']
        q.enqueue(dos_status_monitor.check_single_service,
                  service_id,
                  ttl=f'{config.CHECK_RATE_MINUTES}m')
        service_job_count += 1
    print(f'Added {service_job_count} service jobs to the queue')


def add_service_status_job():
    q.enqueue(slack.send_slack_status_update,
              ttl=f'{config.STATUS_UPDATE_RATE_MINUTES}m')
    print('Added Slack status update to the queue')


add_search_jobs()
add_service_jobs()
add_service_status_job()

schedule.every(config.CHECK_RATE_MINUTES).minutes\
    .do(add_search_jobs)
schedule.every(config.CHECK_RATE_MINUTES).minutes\
    .do(add_service_jobs)
schedule.every(config.STATUS_UPDATE_RATE_MINUTES).minutes\
    .do(add_service_status_job)

print(f"{len(probes.get_probe_list())} probes configured to run "
      f"every {config.CHECK_RATE_MINUTES} minute(s).")

print("Slack Status Summary will run every "
      f"{config.STATUS_UPDATE_RATE_MINUTES} minute(s).")

try:
    while True:
        print(f"Ping!")
        schedule.run_pending()
        time.sleep(60)
except:
    rollbar.report_exc_info()
