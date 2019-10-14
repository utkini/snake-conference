import logging
from enum import Enum

"""
Rename __name__ and copy file to player_1.py, player_2.py ...
Run sample_run.py 
"""
__name__ = 'blabla_1'


log = logging.getLogger(__name__)


class PlayerAction(Enum):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1


class PlayerDirection(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def dec_log(func):
    def wrapper(s, *args, **kwargs):
        r = func(s, *args, **kwargs)
        log.debug('Direction: {0}. action: {1}, args: {2}'.format(s.direction, r, args))
        return r
    return wrapper


class Player:
    def __init__(self):
        self.direction = PlayerDirection.UP

    @dec_log
    def next_step(self, game_map, player_head_coordinate):
        x, y = player_head_coordinate
        h_edge = 0
        w_edge = 0
        if not x:
            h_edge = -1
        elif x == len(game_map) - 1:
            h_edge = 1

        if not y:
            w_edge = -1
        elif y == len(game_map[0]) - 1:
            w_edge = 1
        log.debug(f'h_edge: {h_edge}, w_edge: {w_edge}')
        if h_edge == -1 and w_edge == -1:
            if self.direction == PlayerDirection.UP:
                self.direction = PlayerDirection.RIGHT
                return PlayerAction.RIGHT.value
            elif self.direction == PlayerDirection.LEFT:
                self.direction = PlayerDirection.DOWN
                return PlayerAction.LEFT.value
        elif h_edge == 1 and w_edge == 1:
            if self.direction == PlayerDirection.DOWN:
                self.direction = PlayerDirection.LEFT
                return PlayerAction.RIGHT.value
            elif self.direction == PlayerDirection.RIGHT:
                self.direction = PlayerDirection.UP
                return PlayerAction.LEFT.value

        elif h_edge == 1 and w_edge == -1:
            if self.direction == PlayerDirection.DOWN:
                self.direction = PlayerDirection.RIGHT
                return PlayerAction.LEFT.value
            elif self.direction == PlayerDirection.LEFT:
                self.direction = PlayerDirection.UP
                return PlayerAction.RIGHT.value

        elif h_edge == -1 and w_edge == 1:
            if self.direction == PlayerDirection.UP:
                self.direction = PlayerDirection.LEFT
                return PlayerAction.LEFT.value
            elif self.direction == PlayerDirection.RIGHT:
                self.direction = PlayerDirection.DOWN
                return PlayerAction.RIGHT.value

        elif h_edge == 1 and self.direction == PlayerDirection.DOWN:
            self.direction = PlayerDirection.LEFT
            return PlayerAction.RIGHT.value
        elif w_edge == -1 and self.direction == PlayerDirection.LEFT:
            self.direction = PlayerDirection.UP
            return PlayerAction.RIGHT.value
        elif h_edge == -1 and self.direction == PlayerDirection.UP:
            self.direction = PlayerDirection.RIGHT
            return PlayerAction.RIGHT.value
        elif w_edge == 1 and self.direction == PlayerDirection.RIGHT:
            self.direction = PlayerDirection.DOWN
            return PlayerAction.RIGHT.value

        return PlayerAction.STRAIGHT.value
