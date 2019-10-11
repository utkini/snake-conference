from collections import deque
from enum import Enum


class PlayerAction(Enum):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1


class PlayerDirection(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class BasePlayer:
    def __init__(self, name: str, _hash: str):
        self.name = name
        self.hash = _hash
        self.snake = deque()

        self.__direction = PlayerDirection.UP

        self.__score = 0

    def change_direction(self, action: PlayerAction) -> PlayerDirection:
        if action == PlayerAction.STRAIGHT:
            return self.__direction

        elif action == PlayerAction.LEFT:
            direction = self.__direction.value - 1
            if direction < 0:
                direction = max(PlayerDirection.__members__.values(), key=lambda el: el.value)
            self.__direction = PlayerDirection(direction)

        elif action == PlayerAction.RIGHT:
            direction = self.__direction.value + 1
            if direction > max(PlayerDirection.__members__.values(), key=lambda el: el.value).value:
                direction = 0
            self.__direction = PlayerDirection(direction)

        return self.__direction

    def get_index_head(self):
        return self.snake[0] if self.snake else None

    def get_index_tail(self):
        return self.snake[-1] if self.snake else None

    def delete_tail(self):
        if self.snake:
            self.snake.pop()

    def move(self, index_head: int):
        self.extend(index_head)
        self.delete_tail()

    def extend(self, index_head: int):
        self.snake.appendleft(index_head)

    def increment_score(self):
        self.__score += 1

    def get_score(self):
        return self.__score

    def next_step(self, game_map):
        raise NotImplementedError('Need to implement next_step')

    def serialize(self):
        return {'hash': self.hash, 'name': self.name}


class SimpleTestPlayer(BasePlayer):
    _steps = (PlayerAction.LEFT.value, PlayerAction.RIGHT.value, PlayerAction.STRAIGHT.value, PlayerAction.STRAIGHT.value,
              PlayerAction.STRAIGHT.value)
    steps = iter(_steps)

    def next_step(self, game_map):
        try:
            return next(self.steps)
        except (StopIteration, ) as exc:
            self.steps = iter(self._steps)
            return next(self.steps)


class SimpleTestPlayer1(SimpleTestPlayer):
    _steps = (PlayerAction.LEFT.value, PlayerAction.STRAIGHT.value, PlayerAction.RIGHT.value, PlayerAction.STRAIGHT.value,
              PlayerAction.RIGHT.value)
    steps = iter(_steps)


class SimpleTestPlayer2(SimpleTestPlayer):
    _steps = (PlayerAction.LEFT.value, PlayerAction.STRAIGHT.value, PlayerAction.STRAIGHT.value, PlayerAction.RIGHT.value,
              PlayerAction.STRAIGHT.value)
    steps = iter(_steps)
