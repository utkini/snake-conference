from itertools import cycle

import pytest

from game.game_map import PointState, GameMap
from game.game_players_loader import ClassPlayersLoader
from settings import HEIGHT_MAP, WIDTH_MAP
from game.player import SimpleTestPlayer1, SimpleTestPlayer2


@pytest.fixture(scope='class')
def players(amount=2, name_prefix='test'):
    cycle_classes = cycle((SimpleTestPlayer1, SimpleTestPlayer2))
    classes = [next(cycle_classes) for _ in range(amount)]
    pl_loader = ClassPlayersLoader(classes=classes)

    return pl_loader.get_players()


class TestGameMap:

    def test_initial_points(self, players):
        gm = GameMap(HEIGHT_MAP, WIDTH_MAP, players)
        assert len(list(filter(lambda p: p.state == PointState.SCORE, gm.points))) == gm.amount_scores

    def test_add_score_points(self, players):
        gm = GameMap(HEIGHT_MAP, WIDTH_MAP, players)
        gm.add_score_point()
        assert len(list(filter(lambda p: p.state == PointState.SCORE, gm.points))) == gm.amount_scores

    def test_serialize(self, players):
        height_map = 5
        width_map = 4
        gm = GameMap(height_map, width_map, players)
        serialized = gm.serialize()
        assert len(serialized) == height_map
        assert len(serialized[0]) == width_map
