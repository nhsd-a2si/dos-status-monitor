web: gunicorn -b "0.0.0.0:$PORT" capmon_api.api:app --log-file -
worker: python -u worker.py
clock: python -u clock.py
