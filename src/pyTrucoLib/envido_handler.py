from .state import State
from .utils import get_response

STATE_ENVIDO = 1
STATE_REAL_ENVIDO = 2
STATE_FALTA_ENVIDO = 3
STATE_FINALIZADO = 4

SI = 1
NO = 0


class envido_handler(State):
    _game_instance = None
    _history: list = []
    # Indica quien fue el jugador que canto la primera ves.
    _points: int = 0  # Indica la cantidad de puntos sumados en el envido.
    _last_chant: int = 0  # Indica cual es el ultimo usuario en cantar.
    _loop_envido: bool = False  # Inidica nos encontramos en el loop de envido.

    def __init__(self, gameInstance):
        self._game_instance = gameInstance
        self._actions_map: dict = {
            'envido': self.envido_handler,
            'real_envido': self.real_envido_handler,
            'falta_envido': self.falta_envido_handler,
            'quiero': self.quiero_handler,
        }

    def _general_envido_logic(new_state: int):  # noqa
        def decorator(func):
            def wrapper(*args):
                self = args[0]
                player = args[1]
                self.state = new_state
                if self._game_instance._truco_handler.state > 0:
                    raise ValueError(
                        'No puedes cantar envido despues del truco',
                    )
                if self._game_instance.handNumber != 1:
                    raise ValueError('No podes cantar envido en esta mano')

                func(*args)

                self._game_instance.signals_handler.envido(player)
                self._last_chant = player
                if not self._loop_envido:
                    self.loopEnvido()
            return wrapper
        return decorator

    @_general_envido_logic(STATE_ENVIDO)
    def envido_handler(self, player, *args):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y
         inicia el loop de envido
        :param player:
        '''
        self._points += 2

    @_general_envido_logic(STATE_REAL_ENVIDO)
    def real_envido_handler(self, player, *args):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y
        inicia el loop de envido
        :param player:
        '''
        self._points += 3

    @_general_envido_logic(STATE_FALTA_ENVIDO)
    def falta_envido_handler(self, player, *args):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y
        inicia el loop de envido
        :param player:
        '''
        self._points += 15

    def quiero_handler(self, player, decision):
        if decision == SI:
            self._game_instance.signals_handler.quiero(player)
            self.getWinnerEnvido()
        else:
            self._game_instance.signals_handler.noquiero(player)
            self._game_instance.signals_handler.showWinnerEnvido(
                self._last_chant,
            )
            self._game_instance.givePointsTeam(self._last_chant.getTeam(), 1)
        self.state = STATE_FINALIZADO

    def loopEnvido(self):
        ''' Esta funcion se llama despues de que un jugador canta envido '''
        self._game_instance.signals_handler.startLoopEnvido()
        self._loop_envido = True
        while (self.state is not STATE_FINALIZADO):

            next_player = self._game_instance.getNextTurn(self._last_chant)
            accion_name, accion_values = get_response(
                self._actions_map,
                self._game_instance.signals_handler.getActionPlayer,
                next_player,
                'envido',
            )

            self._actions_map[accion_name](next_player, accion_values)

        self._game_instance.signals_handler.finishLoopEnvido()

    def getWinnerEnvido(self):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y otro
        lo acepta con un quiero
        '''
        winner = {'player': False}
        # Esta variable almacena los puntos ganadores del envido
        tempWinnerPoints = 0
        cJugadas = 0
        # self._game_instance.setTurn(self._game_instance.hand)
        for player in self._game_instance.players:
            cJugadas += 1
            # player = self._game_instance.getTurnAndChange()
            self._game_instance.signals_handler.showEnvido(
                player,
            )  # El jugador canta sus tantos
            if tempWinnerPoints < player.getPointsEnvido():
                winner = player
            tempWinnerPoints = player.getPointsEnvido()
        self._game_instance.signals_handler.showWinnerEnvido(winner)
        self._game_instance.givePointsTeam(
            winner.getTeam(), self._points,
        )  # Se le asigna los puntos del envido al equipo ganador
