import json
import os

from flask import Flask, jsonify, Response
from werkzeug.exceptions import abort

import settings

API_PREFIX = '/api'

app = Flask(__name__)


@app.route('/')
def hello():
    abort(404)


@app.route(f'{API_PREFIX}/log/')
def game_logs():
    result_json = []

    if not os.path.isdir(settings.GAME_LOG_DIR):
        return jsonify(result_json)

    log_files = filter(lambda n: n.endswith(settings.LOG_FILE_POSTFIX), os.listdir(settings.GAME_LOG_DIR))
    for log_file in log_files:
        with open(os.path.join(settings.GAME_LOG_DIR, log_file)) as fd:
            log_json = json.load(fd)
            game_players = log_json.get('players')
            result_json.append({'players': game_players, 'game_log_id': log_file.rstrip(settings.LOG_FILE_POSTFIX),
                                'endTime': log_json.get('endTime'), 'startTime': log_json.get('startTime')})

    return jsonify(result_json)


@app.route(f'{API_PREFIX}/log/<string:game_log_id>/')
def game_log(game_log_id: str):

    if not game_log_id.isalnum():
        abort(400)

    log_filename = f'{game_log_id}{settings.LOG_FILE_POSTFIX}'
    log_file_path = os.path.join(settings.GAME_LOG_DIR, log_filename)

    if not os.path.isfile(log_file_path):
        abort(404)

    with open(log_file_path) as fd:
        return Response(fd.read(), mimetype='application/json')


if __name__ == '__main__':
    app.run()
