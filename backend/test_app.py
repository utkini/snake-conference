import json
import os
import random
import string

import pytest

import settings
from app import app, API_PREFIX


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@pytest.fixture
def game_log_id():
    letters = string.digits + string.ascii_lowercase
    game_log_id = ''.join(random.choice(letters) for _ in range(20))
    content = {"players": {
        "f6f4061a1bddc1c04d8109b39f581270": {
            "hash": "f6f4061a1bddc1c04d8109b39f581270",
            "name": "test0"
        },
        "5a105e8b9d40e1329780d62ea2265d8a": {
            "hash": "5a105e8b9d40e1329780d62ea2265d8a",
            "name": "test1"
        }
    },
        "steps": [],
        "startTime": 1570740903,
        "endTime": 1570740903
    }

    file_path = os.path.join(settings.GAME_LOG_DIR, f'{game_log_id}{settings.LOG_FILE_POSTFIX}')

    with open(file_path, 'wt') as fd:
        fd.write(json.dumps(content))

    yield game_log_id

    try:
        os.remove(file_path)
    except (FileNotFoundError, ):
        pass


def test_root(client):
    resp = client.get('/')
    assert resp.status_code == 404


def test_game_logs(client):
    resp = client.get(f'{API_PREFIX}/log/')

    assert resp.status_code == 200


def test_game_log(client, game_log_id):

    resp = client.get(f'{API_PREFIX}/log/{game_log_id}/')

    assert resp.status_code == 200
