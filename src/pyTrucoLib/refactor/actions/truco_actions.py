from pyTrucoLib.refactor.actions.action import Action
from pyTrucoLib.refactor.actions.jugar_carta_action import jugar_carta


class quiero_truco(Action):
    @classmethod
    def name(cls):
        return "quiero"

    def execute(self, *args):
        self.truco_manager.quiero_expected = False
        self.truco_manager.quiero_player = self.player
        if isinstance(self.from_action, truco):
            self._availables_next_actions = {jugar_carta, re_truco}
        elif isinstance(self.from_action, re_truco):
            self._availables_next_actions = {jugar_carta, vale_4}
        elif isinstance(self.from_action, vale_4):
            self._availables_next_actions = {jugar_carta}
        return super().execute(*args)


class no_quiero_truco(Action):
    @classmethod
    def name(cls):
        return "no_quiero"
    
    def execute(self, *args):
        print(self.player, "perdio")
        list(self.game.teams - {self.player.team})[0].givePoints(self.truco_manager.points-1)
        return ('truco_no_quiero', self.player, None)


DEFAULT_TRUCO_ACTIONS = {quiero_truco, no_quiero_truco}

class vale_4(Action):
    _availables_next_actions = DEFAULT_TRUCO_ACTIONS

    def execute(self, action_value):
        self.truco_manager.points = 4
        self.truco_manager.quiero_expected = True
        return super().execute(action_value)


class re_truco(Action):
    _availables_next_actions = {vale_4} | DEFAULT_TRUCO_ACTIONS

    def execute(self, action_value):
        self.truco_manager.points = 3
        self.truco_manager.quiero_expected = True
        return super().execute(action_value)


class truco(Action):
    _availables_next_actions = {re_truco} | DEFAULT_TRUCO_ACTIONS

    def execute(self, action_value):
        self.truco_manager.points = 2
        self.truco_manager.cantado = True
        self.truco_manager.quiero_expected = True
        return super().execute(action_value)


TRUCO_ACTIONS = {truco, re_truco, vale_4}