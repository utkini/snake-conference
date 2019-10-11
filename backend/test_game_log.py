import hashlib
import shutil

import os
from itertools import cycle

import pytest

import settings
from game.game_log import SnakeGameLog
from game.play import SnakeGame
from game.player import SimpleTestPlayer1, SimpleTestPlayer2


@pytest.fixture(scope='class')
def players(amount=2, name_prefix='test'):
    result = {}
    pl_classes = cycle((SimpleTestPlayer1, SimpleTestPlayer2))
    for num in range(amount):
        pl_name = "{0}{1}".format(name_prefix, num)
        pl_hash = hashlib.md5(pl_name.encode()).hexdigest()
        pl_class = next(pl_classes)
        result[pl_hash] = pl_class(pl_name, pl_hash)

    return result


@pytest.fixture
def clear_game_logs():
    shutil.rmtree(settings.GAME_LOG_DIR, ignore_errors=True)
    yield
    shutil.rmtree(settings.GAME_LOG_DIR, ignore_errors=True)
    os.makedirs(settings.GAME_LOG_DIR)


class TestGameLog:

    def test_save(self, players, clear_game_logs):

        sg = SnakeGame(players)
        sg.run()
        SnakeGameLog(sg).save()

        assert len(os.listdir(settings.GAME_LOG_DIR)) == 1
