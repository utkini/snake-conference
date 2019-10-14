import logging
import random
import typing
from copy import copy
from enum import Enum

import settings

if typing.TYPE_CHECKING:
    from .player import BasePlayer


log = logging.getLogger(__name__)


class MapState(Enum):
    PLAY = 0
    CRASH = 1
    SCORE = 2
    END_SCORES = 3


class PointState(Enum):
    EMPTY = 0
    SNAKE = 1
    SCORE = 2


CRASH_POINT_STATES = {PointState.SNAKE}
SCORE_POINT_STATES = {PointState.SCORE}


class Point:
    def __init__(self, state: PointState, player: typing.Optional['BasePlayer']=None):
        self.state = state
        self.player = player

        if player is not None:
            self.state = PointState.SNAKE

    def visit(self, player: 'BasePlayer') -> PointState:
        prev_state = self.state
        self.player = player
        self.state = PointState.SNAKE
        return prev_state

    def clear(self):
        self.state = PointState.EMPTY
        self.player = None

    def __repr__(self):
        return f'State: {self.state}, player: {self.player}'

    def serialize(self):
        return {'state': self.state.value, 'player': self.player.hash if self.player else None}

    def __eq__(self, other: 'Point'):
        return self.state == other.state and self.player == other.player


class GameMap:
    def __init__(self, height: int, width: int, players: typing.Dict):
        self.height = height
        self.width = width
        self.players = players

        self.amount_scores = self.initialize_amount_scores()
        self.left_scores = settings.GAME_SCORES

        self.points = self.initialize_points()

    def initialize_amount_scores(self) -> int:
        # return random.randint(1, (self.width * self.height - len(self.players)) // 2)
        return 1

    def add_score_point(self) -> bool:
        if len(tuple(filter(lambda p: p.state == PointState.SCORE, self.points))) < self.amount_scores:
            point = random.choice(tuple(filter(lambda p: p.state == PointState.EMPTY, self.points)))
            point.state = PointState.SCORE
            return True
        return False

    def initialize_points(self):
        points = [Point(PointState.SCORE) for _ in range(self.amount_scores)]
        points.extend([Point(PointState.SNAKE, player) for player in self.players.values()])
        points.extend([Point(PointState.EMPTY)
                       for _ in range(self.width * self.height - len(self.players) - self.amount_scores)])
        random.shuffle(points)

        log.debug('Points: %s', points)

        return points

    def find_player_position(self, player) -> typing.Optional[int]:
        # ToDo more smart finder
        for point_index, point in enumerate(self.points):
            if point.player is not None and point.player == player:
                return point_index
        return None

    def move_point_right(self, point_index):
        dst_point_index = point_index + 1
        if (point_index % self.width) == self.width - 1:
            return MapState.CRASH, dst_point_index

        return self.__move_snake_point(point_index, dst_point_index), dst_point_index

    def move_point_left(self, point_index):
        dst_point_index = point_index - 1
        if point_index % self.width == 0 or not point_index:
            return MapState.CRASH, dst_point_index

        return self.__move_snake_point(point_index, dst_point_index), dst_point_index

    def move_point_up(self, point_index):
        dst_point_index = point_index - self.width

        if point_index < self.width:
            return MapState.CRASH, dst_point_index
        return self.__move_snake_point(point_index, dst_point_index), dst_point_index

    def move_point_down(self, point_index):
        dst_point_index = point_index + self.width
        if (point_index + self.width) >= len(self.points):
            return MapState.CRASH, dst_point_index

        return self.__move_snake_point(point_index, dst_point_index), dst_point_index

    def __move_snake_point(self, src_index: int, dst_index: int) -> MapState:
        log.debug('DST: {}'.format(dst_index))
        dst_point = self.points[dst_index]
        src_point = self.points[src_index]

        result = MapState.PLAY
        if dst_point.state in CRASH_POINT_STATES:
            result = MapState.CRASH
        elif dst_point.state in SCORE_POINT_STATES:
            self.left_scores -= 1
            if self.left_scores:
                self.add_score_point()
            result = MapState.SCORE

        self.points[dst_index] = copy(src_point)

        return result

    def clear_point(self, point_index):
        self.points[point_index].clear()

    def get_state(self) -> MapState:
        return MapState.CRASH

    def serialize(self):
        serialized_points = []
        for line in range(self.height):
            shift = line * self.width
            serialized_points.append([p.serialize() for p in self.points[shift:shift + self.width]])
        return serialized_points

    def convert_point_index_to_coordinate(self, point_index: int) -> typing.Tuple[int, int]:
        return point_index // self.width, point_index % self.width

    def __str__(self):
        return 'Class: {0}. Map\n{1}'.format(self.__class__, '\n'.join(map(str, self.serialize())))

    def __eq__(self, other: 'GameMap'):
        return self.points == other.points
