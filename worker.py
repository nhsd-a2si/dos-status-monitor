import check
import config
import datetime
import schedule
import time

print(f"Checking for types {config.UEC_DOS_SERVICE_TYPES} every {config.CHECK_RATE_MINUTES} minute(s)")


schedule.every(config.CHECK_RATE_MINUTES).minutes.do(check.job)

check.job()

while True:
    print(f"Ping! {datetime.datetime.utcnow()}")
    schedule.run_pending()
    time.sleep(30)
