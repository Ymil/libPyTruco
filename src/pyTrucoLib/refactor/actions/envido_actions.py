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
        winner = None
        # Esta variable almacena los puntos ganadores del envido
        tempWinnerPoints = 0
        cJugadas = 0
        for player in self.game.players:
            cJugadas += 1
            # self._game_instance.table.signals_handler.showEnvido(
            #     player,
            # )  # El jugador canta sus tantos
            if tempWinnerPoints < player.getPointsEnvido():
                winner = player
            tempWinnerPoints = player.getPointsEnvido()
        winner.getTeam().givePoints(self.envido_manager.points)
        print(f'{winner} gano el envido con {winner.getPointsEnvido()} puntos')
        return super().execute(action_value)


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

