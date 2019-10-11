import hashlib
import shutil

import os
from itertools import cycle

import pytest

import settings
from game.game_log import SnakeGameLog
from game.game_players_loader import ClassPlayersLoader
from game.play import SnakeGame
from game.player import SimpleTestPlayer1, SimpleTestPlayer2


@pytest.fixture(scope='class')
def players(amount=2, name_prefix='test'):
    cycle_classes = cycle((SimpleTestPlayer1, SimpleTestPlayer2))
    classes = [next(cycle_classes) for _ in range(amount)]
    pl_loader = ClassPlayersLoader(classes=classes)

    return pl_loader.get_players()


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
