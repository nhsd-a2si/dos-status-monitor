from flask import Flask
from flask import jsonify

app = Flask(__name__)

from dos_status_monitor import database


@app.route('/statuses')
def get_statuses():
    statuses = database.get_service_statuses()
    print(statuses)
    return jsonify(statuses)


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0')
