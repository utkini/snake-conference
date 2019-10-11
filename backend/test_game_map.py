import pytest

from game.game_map import PointState, GameMap
from settings import HEIGHT_MAP, WIDTH_MAP
from game.player import BasePlayer


@pytest.fixture(scope='class')
def players():
    return {'test': BasePlayer('test', 'test'), 'test1': BasePlayer('test1', 'test1')}


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
