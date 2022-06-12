from dataclasses import dataclass
from enum import Enum
from itertools import cycle
from typing import List
from typing import Set
from unittest import signals

from pyTrucoLib.controllers.controller import Controler
from pyTrucoLib.controllers.round_controller import round_controller
from pyTrucoLib.handlers.signals import signals
from pyTrucoLib.player import Player
from pyTrucoLib.team import Team

from ..actions.functions import get_action


class TurnManager:
    def __init__(self, players):
        self.players = players
        self.current_idx = -1

    def next(self):
        self.current_idx += 1
        if self.current_idx >= len(self.players):
            self.current_idx = 0
        return self.players[self.current_idx]

    def next_without_changes(self):
        idx = self.current_idx + 1
        if idx >= len(self.players):
            idx = 0
        return self.players[idx]

    def set_next(self, player):
        self.current_idx = self.get_index_for_next(player)

    def get_index_for_next(self, player):
        current_idx = self.players.index(player)
        if current_idx == 0:
            current_idx = len(self.players) - 1
        else:
            current_idx -= 1
        return current_idx

    def set_next_from_player(self, player):
        self.set_next(player)
        next(self)

    def get_current(self):
        return self.players[self.current_idx]

    def __next__(self):
        return self.next()


class game_mediator:
    def __init__(self):
        self.game = None
        self.round = None
        self.hand = None
        self.truco_manager = None
        self.envido_manager = None
        self.turn_manager = None
        self.get_action = None

    def set_game(self, game):
        self.game = game
        self.signals = self.game.signals

    def set_round(self, round):
        self.round = round
        self.truco_manager = self.round.truco_manager
        self.envido_manager = self.round.envido_manager

    def set_hand(self, hand):
        self.hand = hand

    def set_turn_manager(self, turn_manager):
        self.turn_manager = turn_manager

    def set_funcion_get_action(self, funcion):
        self.get_action = funcion


@dataclass
class game_controller(Controler):
    teams: Set
    players: List
    signals: str = None

    def __post_init__(self):
        self.GM = game_mediator()
        self.GM.set_game(self)
        self.GM.set_turn_manager(
            TurnManager(self.players),
        )
        self.GM.set_funcion_get_action(
            get_action,
        )

    def start(self):

        self.GM.signals.showMsgStartGame()
        while True:
            start_player_round = self.GM.turn_manager.next_without_changes()
            round_controller(self.GM).start()
            self.GM.turn_manager.set_next_from_player(start_player_round)
            if self.search_winner():
                break
        self.GM.signals.showMsgFinishGame()

    def search_winner(self) -> bool:
        for team in self.teams:
            if team.getPoints() >= 30:
                self.GM.signals.winGameTeam(team)
                return True
        return False
