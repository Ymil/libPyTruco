from pyTrucoLib.actions.action import Action
from pyTrucoLib.actions.jugar_carta_action import jugar_carta


class quiero_truco(Action):
    @classmethod
    def name(cls):
        return 'quiero'

    def execute(self, *args):
        self.GM.turn_manager.set_next(self.GM.truco_manager.start_player)
        self.GM.truco_manager.start_player = None
        self.GM.truco_manager.quiero_expected = False
        self.GM.truco_manager.quiero_player = self.player
        self.GM.signals.quiero(self.player)
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
        return 'no_quiero'

    def execute(self, *args):

        winner_team = list(self.GM.game.teams - {self.player.team})[0]
        winner_team.givePoints(self.GM.truco_manager.points-1)
        self.GM.signals.noquiero(self.player)
        self.GM.signals.win(winner_team.getID())
        return ('truco_no_quiero', self.player, None)


DEFAULT_TRUCO_ACTIONS = {quiero_truco, no_quiero_truco}


class vale_4(Action):
    _availables_next_actions = DEFAULT_TRUCO_ACTIONS

    def execute(self, action_value):
        if self.GM.truco_manager.start_player is None:
            self.GM.truco_manager.start_player = self.player
        self.GM.truco_manager.next_availables_actions = set()
        self.GM.truco_manager.points = 4
        self.GM.truco_manager.quiero_expected = True
        self.GM.signals.vale_4(self.player)
        return super().execute(action_value)


class re_truco(Action):
    _availables_next_actions = {vale_4} | DEFAULT_TRUCO_ACTIONS

    def execute(self, action_value):
        if self.GM.truco_manager.start_player is None:
            self.GM.truco_manager.start_player = self.player
        self.GM.truco_manager.next_availables_actions = {vale_4}
        self.GM.truco_manager.points = 3
        self.GM.truco_manager.quiero_expected = True
        self.GM.signals.retruco(self.player)
        return super().execute(action_value)


class truco(Action):
    _availables_next_actions = {re_truco} | DEFAULT_TRUCO_ACTIONS

    def execute(self, action_value):
        if self.GM.truco_manager.start_player is None:
            self.GM.truco_manager.start_player = self.player
        self.GM.truco_manager.next_availables_actions = {re_truco}
        self.GM.truco_manager.points = 2
        self.GM.truco_manager.cantado = True
        self.GM.truco_manager.quiero_expected = True
        self.GM.signals.truco(self.player)
        return super().execute(action_value)


TRUCO_ACTIONS = {truco, re_truco, vale_4}
