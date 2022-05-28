from action import Action
from jugar_carta_action import jugar_carta
from truco_actions import *

class quiero_envido(Action):
    _availables_next_actions = {jugar_carta, truco}

    @classmethod
    def name(cls):
        return "quiero"


class no_quiero_envido(Action):
    _availables_next_actions = {jugar_carta, truco}

    @classmethod
    def name(cls):
        return "no_quiero"


DEFAULT_ENVIDO_ACTIONS = {quiero_envido, no_quiero_envido}


class falta_envido(Action):
    _availables_next_actions = DEFAULT_ENVIDO_ACTIONS


class real_envido(Action):
    _availables_next_actions = {falta_envido} | DEFAULT_ENVIDO_ACTIONS

    def execute(self, action_value):
        self._availables_next_actions = self._availables_next_actions | {eval("envido")}
        return super().execute(action_value)

class envido(Action):
    _availables_next_actions = {real_envido, falta_envido} | DEFAULT_ENVIDO_ACTIONS

    def execute(self, action_value):
        self._availables_next_actions = self._availables_next_actions | {eval("envido")}
        return super().execute(action_value)

