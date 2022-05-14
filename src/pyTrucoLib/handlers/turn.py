from copy import copy
from itertools import cycle
from typing import Any
from typing import List


class TurnHandler(list):
    """
    Clsae encargada de las gestion de los turnos de los jugadores
    """
    _players: List[Any] = []
    _players_order: List[Any] = []

    def __init__(self, players: List[Any]):
        self._players = copy(players)
        self._players_order = copy(players)

    def change_hand(self, player):
        idx_player = self._players.index(player)
        player_infinity = cycle(self._players)
        initial_post = idx_player
        finally_post = idx_player+len(self._players)
        self._players_order = []
        for idx in range(0, finally_post):
            player = next(player_infinity)
            if(idx >= initial_post):
                self._players_order.append(player)

    def change_round(self):
        player_infinity = cycle(self._players)
        initial_post = 1
        finally_post = 1+len(self._players)
        self._players = []
        for idx in range(0, finally_post):
            player = next(player_infinity)
            if(idx >= initial_post):
                self._players.append(player)

    def __getitem__(self, index):
        return self._players_order[index]

    def __iter__(self):
        yield from self._players_order
