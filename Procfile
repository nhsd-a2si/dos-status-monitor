web: gunicorn -b "0.0.0.0:$PORT" capmon_api.api:app --log-file -
worker: python worker.py
clock: python clock.py
