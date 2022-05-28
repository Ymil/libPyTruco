from abc import ABC
from itertools import cycle
from pyTrucoLib.refactor.actions.action import Action
from pyTrucoLib.refactor.actions.envido_actions import envido, real_envido, falta_envido
from pyTrucoLib.refactor.actions.functions import get_action
from pyTrucoLib.refactor.actions.truco_actions import truco
from pyTrucoLib.refactor.actions.jugar_carta_action import jugar_carta

class initial_action(Action):
    _availables_next_actions = {
        jugar_carta,
    }

    def __init__(self, game, round, hand, get_action_function, player):
        self.from_action = None
        self.truco_manager = round._truco_manager
        self.envido_manager = round._envido_manager
        self.get_action_func = get_action_function
        self.game = game
        self.hand = hand
        self.round = round
        self.player = player
        if self.truco_manager.cantado:
            self._availables_next_actions = self._availables_next_actions | self.truco_manager.next_availables_actions
        else:
            self._availables_next_actions = self._availables_next_actions | {
                truco,
            }
        if self.hand.number == 1:
            self._availables_next_actions = self._availables_next_actions | {
                envido, real_envido, falta_envido
            }
