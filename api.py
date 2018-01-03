from flask import Flask
from flask import jsonify
from flask_basicauth import BasicAuth

app = Flask(__name__)


from dos_status_monitor import database, logger, config

app.config['BASIC_AUTH_USERNAME'] = config.BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = config.BASIC_AUTH_PASSWORD
app.config['BASIC_AUTH_FORCE'] = config.BASIC_AUTH_FORCE

basic_auth = BasicAuth(app)


@app.route('/statuses')
def get_statuses():
    statuses = database.get_service_statuses()
    count = len(statuses)
    logger.info(f"REQUEST /statuses {count} records")
    return jsonify(statuses)


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0')
