import requests
import time
from flask import Flask
from flask import request
from flask import json

from mpu6050 import record_data
from analysis import analyse_data

app = Flask(__name__)


@app.route('/startDrill', methods=['POST'])
def start_drill():
    data = request.get_json()

    exec_time = data['exec_time']
    drill_id = data['drill_id']
    recorded_data = record_data(execution_time=exec_time, frequency=10)
    result = analyse_data(recorded_data, drill_id % 3, frequency=10)
    return app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
