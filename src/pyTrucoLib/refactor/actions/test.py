



from abc import ABC
from itertools import cycle
from envido_actions import *
from pyTrucoLib.refactor.actions.functions import get_action
from truco_actions import *
from jugar_carta_action import jugar_carta
from functions import *

players = cycle(["player1", "player2"])

class points_manager(ABC):
    _points: int = 0

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        print("setter of x called")
        self._points = value

class truco_manager(points_manager):
    quiero_player: str = None
    cantado: bool = False
    quiero_expected = False

class envido_manager(points_manager):
    cantado: bool = True

class round:
    _truco_manager = truco_manager()
    _envido_manager = envido_manager()

class game:
    turn_manager = players
class initial_action(Action):
    _availables_next_actions = {
        jugar_carta, truco, envido, real_envido, falta_envido
    }

    def __init__(self, game, round, get_action_function, player):
        self.from_action = None
        self.truco_manager = round._truco_manager
        self.envido_manager = round._envido_manager
        self.get_action_func = get_action
        self.game = game
        self.player = player
        


def main():
    player = next(players)
    get_action(
        initial_action(game(), round(), get_action, player), 
        player
    )

main()