from abc import ABC
from itertools import cycle
from pyTrucoLib.refactor.actions.envido_actions import *
from pyTrucoLib.refactor.actions.functions import get_action
from pyTrucoLib.refactor.actions.truco_actions import *
from pyTrucoLib.refactor.actions.jugar_carta_action import jugar_carta
from pyTrucoLib.refactor.actions.functions import *

class initial_action(Action):
    _availables_next_actions = {
        jugar_carta, truco, envido, real_envido, falta_envido
    }

    def __init__(self, game, round, hand, get_action_function, player):
        self.from_action = None
        self.truco_manager = round._truco_manager
        self.envido_manager = round._envido_manager
        self.get_action_func = get_action
        self.game = game
        self.hand = hand
        self.round = round
        self.player = player