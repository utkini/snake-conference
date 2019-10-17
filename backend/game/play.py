import logging
import time
import typing
from collections import Counter
from enum import Enum
from itertools import cycle

import settings
from game.game_map import MapState, GameMap
from game.player import PlayerAction, BasePlayer, PlayerDirection

CONTINUE_PLAY_MAP_STATES = (MapState.PLAY, MapState.SCORE)
CRASH_PLAY_MAP_STATES = (MapState.CRASH, )
STOP_PLAY_MAP_STATES = (MapState.END_SCORES, ) + CRASH_PLAY_MAP_STATES
SCORE_MAP_STATES = (MapState.SCORE, MapState.END_SCORES)


AVAILABLE_PLAYER_ACTIONS = {member.value for member in PlayerAction.__members__.values()}


log = logging.getLogger(__name__)


class GameState(Enum):
    PLAYING = 0
    STOPPED = 1


class SnakeGame:
    def __init__(self, players: dict):
        self.players = players
        self.game_map = GameMap(settings.HEIGHT_MAP, settings.WIDTH_MAP, self.players)
        self.game_log = []
        self.game_state = GameState.STOPPED
        self.start_time = None
        self.end_time = None
        self.winner = None
        self.play_iterations = settings.GAME_MAX_ITERATION * len(players)

    def _apply_action_on_map_state(self, player: BasePlayer, map_state: MapState):

        if map_state in SCORE_MAP_STATES:
            player.increment_score()

        if map_state in STOP_PLAY_MAP_STATES:
            self.define_winner(player, map_state)
            self.stop()

    def set_winner(self, player: BasePlayer):
        self.winner = player

    def define_winner(self, current_player: typing.Optional[BasePlayer],
                      map_state: typing.Optional[MapState]) -> typing.Optional[BasePlayer]:
        players = self.players.copy()
        winner = None

        if current_player is not None and map_state == MapState.CRASH and current_player.hash in players:
            players.pop(current_player.hash)

        if players:
            players_scores = {player: player.get_score() for player in players.values()}
            scores = Counter(players_scores.values())
            tmp_winner, max_score = max(players_scores.items(), key=lambda p: p[1])

            if scores[max_score] == 1:
                winner = tmp_winner
                self.set_winner(winner)

        return winner

    def _validate_player_action(self, step_result: int):
        return step_result in AVAILABLE_PLAYER_ACTIONS

    def _move_player(self, player: BasePlayer) -> typing.Optional[MapState]:
        if player.get_index_head() is None:
            player_index_head = self.game_map.find_player_position(player)

            if player_index_head is None:
                return None

            player.extend(player_index_head)

        player_action = player.next_step(self.game_map)

        if not self._validate_player_action(player_action):
            return None

        player_action = PlayerAction(player_action)

        direction = player.change_direction(player_action)
        map_state = None
        dst_index = None
        index_head = player.get_index_head()
        log.debug('Direction: {}'.format(direction))

        if direction == PlayerDirection.UP:
            map_state, dst_index = self.game_map.move_point_up(index_head)
        elif direction == PlayerDirection.RIGHT:
            map_state, dst_index = self.game_map.move_point_right(index_head)
        elif direction == PlayerDirection.LEFT:
            map_state, dst_index = self.game_map.move_point_left(index_head)
        elif direction == PlayerDirection.DOWN:
            map_state, dst_index = self.game_map.move_point_down(index_head)

        log.debug("Player name: {3}. Index head: {4} Snake: {5} Direction: {0}. Dst index: {1}. Map state: {2}".format(
            direction, dst_index, map_state, player.name, index_head, str(player.snake)))

        if map_state is None:
            return map_state

        if map_state not in CRASH_PLAY_MAP_STATES and map_state not in SCORE_MAP_STATES:
            self.game_map.clear_point(player.get_index_tail())
            player.move(dst_index)
        elif map_state in SCORE_MAP_STATES:
            player.extend(dst_index)

        return map_state

    def stop(self):
        self.game_state = GameState.STOPPED
        self.end_time = time.time()
        if self.winner is None:
            self.define_winner(None, None)

    def run(self):
        self.game_state = GameState.PLAYING
        self.start_time = time.time()
        cycle_players = cycle(self.players.values())

        for player in cycle_players:

            self.play_iterations -= 1

            if self.game_state == GameState.STOPPED:
                return

            map_state = self._move_player(player)

            if map_state is None:
                continue

            self._apply_action_on_map_state(player, map_state)

            self.game_log.append(self.game_map.serialize())

            if not self.play_iterations:
                self.stop()
