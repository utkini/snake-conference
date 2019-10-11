import hashlib
import random
from itertools import cycle

import pytest

from game.game_map import GameMap, Point, PointState, MapState
from game.play import SnakeGame, GameState
from game.player import SimpleTestPlayer, PlayerAction


def get_class_player(name, steps):
    return type(name, (SimpleTestPlayer, ), {'_steps': steps, 'steps': iter(steps)})


def generate_steps():
    steps = list(SimpleTestPlayer._steps)
    random.shuffle(steps)
    return tuple(steps)


@pytest.fixture(scope='class')
def players_generator():
    def get_players(amount=1, name_prefix='test', players_steps=None):
        result = {}

        if players_steps is not None:
            players_classes = [
                get_class_player(f'TestPlayer{num_class}', steps)
                for num_class, steps in enumerate(players_steps)
            ]

            pl_classes = cycle(players_classes)
        else:
            pl_classes = (
                get_class_player(f'TestPlayer{num_class}', generate_steps())
                for num_class in range(amount)
            )

        for num in range(amount):
            pl_name = "{0}{1}".format(name_prefix, num)
            pl_hash = hashlib.md5(pl_name.encode()).hexdigest()
            pl_class = next(pl_classes)
            result[pl_hash] = pl_class(pl_name, pl_hash)

        return result

    return get_players


@pytest.fixture()
def map_generator():
    def get_map(points, players):
        width = 2
        for i in range(2, len(points) // 2):
            if len(points) // i == i:
                width = i
                break
        gm = GameMap(width, width, players)
        gm.points = points
        return gm
    return get_map


class TestGamePlay:
    def test_score(self, players_generator, map_generator):
        players = players_generator(players_steps=[[PlayerAction.LEFT.value, ]])

        player_hash, player = tuple(players.items())[0]
        game_map = map_generator([
            Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE),
            Point(PointState.SCORE), Point(PointState.SNAKE, player), Point(PointState.SCORE),
            Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE)
        ], players)
        game = SnakeGame(players)
        game.game_map = game_map

        for _ in range(3):
            game._move_player(player)

        expected_map = [
            Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE),
            Point(PointState.SNAKE, player), Point(PointState.SNAKE, player), Point(PointState.SCORE),
            Point(PointState.SNAKE, player), Point(PointState.SNAKE, player), Point(PointState.SCORE)
        ]

        assert expected_map == game.game_map.points

    def test_two_player_score(self, players_generator, map_generator):
        players = players_generator(amount=2, players_steps=[[PlayerAction.LEFT.value, ], [PlayerAction.RIGHT.value, ]])
        (player1_hash, player1), (player2_hash, player2) = tuple(players.items())[:2]
        game_map = map_generator([
            Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE),
            Point(PointState.SNAKE, player2), Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SNAKE, player1),  # noqa
            Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE),
            Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE,)
        ], players)

        game = SnakeGame(players)
        game.game_map = game_map

        for _ in range(3):
            game._move_player(player1)
            game._move_player(player2)

        expected_map = [
            Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE),
            Point(PointState.SNAKE, player2), Point(PointState.SNAKE, player2), Point(PointState.SNAKE, player1), Point(PointState.SNAKE, player1),  # noqa
            Point(PointState.SNAKE, player2), Point(PointState.SNAKE, player2), Point(PointState.SNAKE, player1), Point(PointState.SNAKE, player1),  # noqa
            Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE), Point(PointState.SCORE,)  # noqa
        ]

        assert expected_map == game.game_map.points

    def test_player_steps(self, players_generator, map_generator):
        players = players_generator(amount=1, players_steps=[[PlayerAction.LEFT.value, ], ])
        player1_hash, player1 = tuple(players.items())[0]
        game_map = map_generator([
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.SNAKE, player1),  # noqa
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY,)
        ], players)

        game = SnakeGame(players)
        game.game_map = game_map

        for _ in range(3):
            game._move_player(player1)

        expected_map = [
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),  # noqa
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.SNAKE, player1),
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY, )
        ]

        assert expected_map == game.game_map.points

    def test_player_run(self, players_generator, map_generator):
        players = players_generator(
            amount=1,
            players_steps=[[PlayerAction.LEFT.value, PlayerAction.LEFT.value, PlayerAction.LEFT.value,
                            PlayerAction.STRAIGHT.value], ])
        player1_hash, player1 = tuple(players.items())[0]
        game_map = map_generator([
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.SNAKE, player1),  # noqa
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY,)
        ], players)

        game = SnakeGame(players)
        game.game_map = game_map

        game.run()

        expected_map = [
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),  # noqa
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.SNAKE, player1),
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY, )
        ]

        assert expected_map == game.game_map.points
        assert game.game_state == GameState.STOPPED

    def test_two_player_run(self, players_generator, map_generator):
        player_1_steps = [
            PlayerAction.LEFT.value, PlayerAction.LEFT.value, PlayerAction.LEFT.value, PlayerAction.STRAIGHT.value]
        player_2_steps = [
            PlayerAction.RIGHT.value, PlayerAction.RIGHT.value, PlayerAction.RIGHT.value, PlayerAction.STRAIGHT.value]
        players = players_generator(amount=2, players_steps=[player_1_steps, player_2_steps])
        (player1_hash, player1), (player2_hash, player2) = tuple(players.items())[:2]
        game_map = map_generator([
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),
            Point(PointState.SNAKE, player2), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.SNAKE, player1),  # noqa
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY,)
        ], players)

        game = SnakeGame(players)
        game.game_map = game_map

        game.run()

        expected_map = [
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY),
            Point(PointState.SNAKE, player2), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.SNAKE, player1),  # noqa
            Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY), Point(PointState.EMPTY, )
        ]

        assert expected_map == game.game_map.points
        assert game.game_state == GameState.STOPPED
        assert game.game_map.get_state() == MapState.CRASH
