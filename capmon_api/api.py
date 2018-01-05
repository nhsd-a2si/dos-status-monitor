from flask import Flask
from flask import jsonify, render_template
from flask_basicauth import BasicAuth
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

from dos_status_monitor import database, logger, config

app.config['BASIC_AUTH_USERNAME'] = config.BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = config.BASIC_AUTH_PASSWORD
app.config['BASIC_AUTH_FORCE'] = config.BASIC_AUTH_FORCE

basic_auth = BasicAuth(app)


@app.route('/statuses')
def get_statuses():
    statuses = database.get_all_statuses()
    count = len(statuses)
    logger.info(f"REQUEST /statuses {count} records")
    return jsonify(statuses)


@app.route('/map')
def status_map():
    api_key = config.GOOGLE_MAPS_API_KEY
    data = database.get_all_statuses()
    return render_template('index.html',
                           api_key=api_key,
                           data=data)


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0')