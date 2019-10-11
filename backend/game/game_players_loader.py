import hashlib
import importlib
import importlib.util
import os
import time
import typing

import settings
from game.player import BasePlayer


class BaseLoader:

    def get_players(self) -> dict:
        raise NotImplementedError()

    def _create_player(self, player_name, next_step_obj):
        class_player = type('Player{}'.format(int(time.time())), (BasePlayer,), {'next_step_obj': next_step_obj})
        player_hash = hashlib.md5(player_name.encode()).hexdigest()

        return player_hash, class_player(player_name, player_hash)


class ClassPlayersLoader(BaseLoader):
    def __init__(self, classes: typing.Iterable):
        super(ClassPlayersLoader, self).__init__()
        self.class_list = classes

    def get_players(self) -> dict:
        players = []
        for num_player, class_next_step in enumerate(self.class_list):
            player_name = f'Player{num_player}'

            players.append(self._create_player(player_name, class_next_step()))

        return dict(players)


class FilePlayersLoader(BaseLoader):
    def _validate_module(self, module) -> bool:
        return bool(getattr(module, '__name__', None))

    def get_players(self) -> dict:
        players: typing.List[typing.Tuple] = []
        modules_files = filter(lambda n: n.startswith(settings.PLAYER_FILE_PREFIX),
                               os.listdir(settings.GAME_PLAYERS_DIR))
        for file_player in modules_files:
            module_name = file_player.rstrip('.py')
            package_name = settings.GAME_PLAYERS_DIR_NAME
            module = importlib.import_module(f'{package_name}.{module_name}', module_name)
            if not self._validate_module(module):
                continue
            players.append(self._get_player(module))

        return dict(players)

    def _get_player(self, module):
        class_next_step = getattr(module, 'Player')
        player_name = getattr(module, '__name__')
        next_step_obj = class_next_step()

        return self._create_player(player_name, next_step_obj)


if __name__ == '__main__':
    fl = FilePlayersLoader()
    print(fl.get_players())
