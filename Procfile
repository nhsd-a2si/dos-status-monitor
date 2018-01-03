web: gunicorn -b "0.0.0.0:$PORT" api:app --log-file -
worker: python heroku_worker.py
clock: python heroku_clock.py
