from pyTrucoEngine.actions.action import Action
from pyTrucoEngine.actions.envido_actions import envido
from pyTrucoEngine.actions.envido_actions import falta_envido
from pyTrucoEngine.actions.envido_actions import real_envido
from pyTrucoEngine.actions.jugar_carta_action import jugar_carta
from pyTrucoEngine.actions.truco_actions import truco


class initial_action(Action):
    _availables_next_actions = {
        jugar_carta,
    }

    def __init__(self, game_mediator, player):
        self.GM = game_mediator
        self.player = player
        if self.GM.truco_manager.cantado:
            self._availables_next_actions = self._availables_next_actions | \
                self.GM.truco_manager.next_availables_actions
        else:
            self._availables_next_actions = self._availables_next_actions | {
                truco,
            }
        if self.GM.hand.number == 1:
            self._availables_next_actions = self._availables_next_actions | {
                envido, real_envido, falta_envido,
            }
