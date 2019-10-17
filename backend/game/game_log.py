import hashlib
import json
import os
import typing

import settings
from settings import GAME_LOG_DIR

if typing.TYPE_CHECKING:
    from .play import SnakeGame


class SnakeGameLog:
    def __init__(self, game: 'SnakeGame'):
        self.game = game
        self.serialized_game = self._serialize()

    def _serialize(self) -> dict:
        result = dict()
        result['players'] = {player_hash: player.serialize()
                             for player_hash, player in self.game.players.items()}
        result['steps'] = self.game.game_log
        result['startTime'] = int(self.game.start_time)
        result['endTime'] = int(self.game.end_time)
        result['winner'] = self.game.winner.hash if self.game.winner is not None else None
        return result

    def to_json(self):
        return json.dumps(self._serialize())

    def save(self):

        if not os.path.isdir(GAME_LOG_DIR):
            os.mkdir(GAME_LOG_DIR)

        dir_name = GAME_LOG_DIR
        data = self.to_json()
        filename = '{0}{1}'.format(hashlib.sha256(data.encode()).hexdigest(), settings.LOG_FILE_POSTFIX)
        with open(os.path.join(dir_name, filename), 'wt') as fd:
            fd.write(data)
