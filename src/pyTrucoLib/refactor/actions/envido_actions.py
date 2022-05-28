from pyTrucoLib.refactor.actions.action import Action
from pyTrucoLib.refactor.actions.jugar_carta_action import jugar_carta
from pyTrucoLib.refactor.actions.truco_actions import *

class quiero_envido(Action):
    _availables_next_actions = {jugar_carta, truco}

    @classmethod
    def name(cls):
        return "quiero"

    def execute(self, action_value):
        """ group: envido
        Esta funcion se llama cuando un jugador canta envido y otro
        lo acepta con un quiero
        """
        self.signals.quiero(self.player)
        winner = None
        # Esta variable almacena los puntos ganadores del envido
        tempWinnerPoints = 0
        cJugadas = 0
        for player in self.game.players:
            cJugadas += 1
            self.signals.showEnvido(
                player,
            )  # El jugador canta sus tantos
            if tempWinnerPoints < player.getPointsEnvido():
                winner = player
            tempWinnerPoints = player.getPointsEnvido()
        winner.getTeam().givePoints(self.envido_manager.points)
        self.signals.showWinnerEnvido(winner)
        self.game.turn_manager.set_next(self.envido_manager.start_player)
        return super().execute(action_value)


class no_quiero_envido(Action):
    _availables_next_actions = {jugar_carta, truco}

    @classmethod
    def name(cls):
        return "no_quiero"

    def execute(self, action_value):
        winner = list(self.game.teams - {self.player.team})[0]
        winner.givePoints(1)
        self.signals.noquiero(self.player)
        self.signals.showWinnerEnvido(
            winner
        )
        self.game.turn_manager.set_next(self.envido_manager.start_player)
        return super().execute(action_value)

DEFAULT_ENVIDO_ACTIONS = {quiero_envido, no_quiero_envido}


class falta_envido(Action):
    _availables_next_actions = DEFAULT_ENVIDO_ACTIONS

    def execute(self, action_value):
        if self.envido_manager.start_player is None:
            self.envido_manager.start_player = self.player
        self.signals.falta_envido(self.player)
        return super().execute(action_value)


class real_envido(Action):
    _availables_next_actions = {falta_envido} | DEFAULT_ENVIDO_ACTIONS

    def execute(self, action_value):
        if self.envido_manager.start_player is None:
            self.envido_manager.start_player = self.player
        self.envido_manager.points += 3
        self._availables_next_actions = self._availables_next_actions | {eval("real_envido")}
        self.signals.real_envido(self.player)
        return super().execute(action_value)

class envido(Action):
    _availables_next_actions = {real_envido, falta_envido} | DEFAULT_ENVIDO_ACTIONS

    def execute(self, action_value):
        if self.envido_manager.start_player is None:
            self.envido_manager.start_player = self.player
        self.envido_manager.points += 2
        self._availables_next_actions = self._availables_next_actions | {eval("envido")}
        self.signals.envido(self.player)
        return super().execute(action_value)

