from pyTrucoEngine.actions.action import Action
from pyTrucoEngine.actions.jugar_carta_action import jugar_carta
from pyTrucoEngine.actions.truco_actions import truco


class quiero_envido(Action):
    _availables_next_actions = {jugar_carta, truco}

    @classmethod
    def name(cls):
        return 'quiero'

    def execute(self, action_value):
        """ group: envido
        Esta funcion se llama cuando un jugador canta envido y otro
        lo acepta con un quiero
        """
        self.GM.signals.quiero(self.player)
        for player in self.GM.game.players:
            # Se anuncian los puntos de cada uno de los jugadores
            self.GM.signals.showEnvido(
                player,
            )  # El jugador canta sus tantos

        # Buscando al equipo ganador del envido
        teams = list(self.GM.game.teams)
        team_one = teams[0]
        team_two = teams[1]

        winner_team = None
        if(team_one.get_envido_points() == team_two.get_envido_points()):
            winner_team = self.GM.round.start_player_round.getTeam()
        elif(team_one.get_envido_points() > team_two.get_envido_points()):
            winner_team = team_one
        elif(team_one.get_envido_points() < team_two.get_envido_points()):
            winner_team = team_two

        winner_team.givePoints(self.GM.envido_manager.points)
        self.GM.signals.showWinnerEnvido(winner_team)
        self.GM.turn_manager.set_next(self.GM.envido_manager.start_player)
        return super().execute(action_value)


class no_quiero_envido(Action):
    _availables_next_actions = {jugar_carta, truco}

    @classmethod
    def name(cls):
        return 'no_quiero'

    def execute(self, action_value):
        self.GM.envido_manager.points = 1
        winner_team = list(self.GM.game.teams - {self.player.team})[0]
        winner_team.givePoints(self.GM.envido_manager.points)
        self.GM.signals.noquiero(self.player)
        self.GM.signals.showWinnerEnvido(
            winner_team,
        )
        self.GM.turn_manager.set_next(self.GM.envido_manager.start_player)
        return super().execute(action_value)


DEFAULT_ENVIDO_ACTIONS = {quiero_envido, no_quiero_envido}


class falta_envido(Action):
    _availables_next_actions = DEFAULT_ENVIDO_ACTIONS

    def execute(self, action_value):
        self.GM.envido_manager.cantado = True
        if self.GM.envido_manager.start_player is None:
            self.GM.envido_manager.start_player = self.player
        self.GM.signals.falta_envido(self.player)
        return super().execute(action_value)


class real_envido(Action):
    _availables_next_actions = {falta_envido} | DEFAULT_ENVIDO_ACTIONS

    def execute(self, action_value):
        self.GM.envido_manager.cantado = True
        if self.GM.envido_manager.start_player is None:
            self.GM.envido_manager.start_player = self.player
        self.GM.envido_manager.points += 3
        self._availables_next_actions = self._availables_next_actions | {
            eval('real_envido'),
        }
        self.GM.signals.real_envido(self.player)
        return super().execute(action_value)


class envido(Action):
    _availables_next_actions = {
        real_envido,
        falta_envido,
    } | DEFAULT_ENVIDO_ACTIONS

    def execute(self, action_value):
        self.GM.envido_manager.cantado = True
        if self.GM.envido_manager.start_player is None:
            self.GM.envido_manager.start_player = self.player
        self.GM.envido_manager.points += 2
        self._availables_next_actions = self._availables_next_actions | {
            eval('envido'),
        }
        self.GM.signals.envido(self.player)
        return super().execute(action_value)
