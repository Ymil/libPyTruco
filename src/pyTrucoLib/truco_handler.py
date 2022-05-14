from .jugador import Jugador
from .state import State
from .team import Team
from .utils import get_response
STATE_TRUCO = 1
STATE_RETRUCO = 2
STATE_VALE_4 = 3
STATE_NO_QUERIDO = 4  # XD

SI = 1
NO = 0


class TrucoNoQuerido(Exception):
    def __init__(self, player, message):
        self.player = player
        self.message = message
        super().__init__(self.message)


class state_decorator(State):
    def _last_state_eq_new_state(self, new_state):
        return self.state == new_state

    def change_status_condicional(self, new_state):
        """
            Se define la condicion para cambiar de status
        """
        return (
            new_state >= self.state and
            new_state - 1 == self.state  # Esta condicion solo permite que
            # se cante el TRUCO en primer lugar, RETRUCO en segunda y
            # VALE 4 en tercera.
        )


class truco_handler(state_decorator):
    # Indica cual es equipo que puede volver a canta
    _quiero_team: Team = None  # noqa
    _points: int = 1  # Indica la cantidad de puntos sumados en el truco.
    _end_state = STATE_NO_QUERIDO

    def __init__(self, gameInstance):
        self._game_instance = gameInstance
        self._actions_map = {
            'truco': self.truco_handler,
            'retruco': self.retruco_handler,
            'vale_4': self.vale4_handler,
            'quiero': self.quiero_handler,
        }

    def _general_truco_logic(new_state: int):
        def decorator(func):
            def wrapper(*args):
                self = args[0]
                player = args[1]

                if self._last_state_eq_new_state(new_state):
                    raise ValueError('No podes volver a cantar')

                self.state = new_state

                if self._quiero_team is not None:
                    if self._quiero_team is not player.team:
                        raise ValueError(
                            'No podes cantar, tu oponente tiene el quiero',
                        )

                func(*args)

                next_player = self._game_instance.getNextTurn(player)
                accion_name, accion_values = get_response(
                    self._actions_map,
                    self._game_instance.signals_handler.getActionPlayer,
                    next_player,
                    'truco',
                )

                self._actions_map[accion_name](next_player, accion_values)
            return wrapper
        return decorator

    @_general_truco_logic(STATE_TRUCO)
    def truco_handler(self, player: Jugador, *args):
        self._game_instance.signals_handler.sendMessageAll(
            f'Jugador {player.getID()} canto truco',
        )
        self._points = 2

    @_general_truco_logic(STATE_RETRUCO)
    def retruco_handler(self, player: Jugador, *args):
        self._game_instance.signals_handler.sendMessageAll(
            f'Jugador {player.getID()} canto retruco',
        )
        self._points = 3

    @_general_truco_logic(STATE_VALE_4)
    def vale4_handler(self, player: Jugador, *args):
        self._game_instance.signals_handler.sendMessageAll(
            f'Jugador {player.getID()} canto vale 4',
        )
        self._points = 4

    def quiero_handler(self, player: Jugador, decision):
        if decision == SI:
            self._game_instance.signals_handler.sendMessageAll(
                f'Jugador {player.getID()} quiso el truco',
            )
            self._quiero_team = player.team
        else:
            self._game_instance.signals_handler.sendMessageAll(
                f'Jugador {player.getID()} no quiso el truco',
            )
            self._points -= 1
            self.freeze()
            raise TrucoNoQuerido(player, '')

    def get_points(self):
        return self._points
