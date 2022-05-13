from multiprocessing.sharedctypes import Value
from shutil import ExecError
from jugador import Jugador
# from juego import Game
from team import Team
from state import State

STATE_TRUCO = 1
STATE_RETRUCO = 2
STATE_VALE_4 = 3
STATE_FINALIZADO = 4

SI = 1
NO = 0

def get_response(actions_maps, callback, *args):
    """
        Ejecuta las consultas hasta que optiene una respuesta correcta
    """
    while 1:
        accion_name, accion_values = callback(*args)
        if accion_name in actions_maps:
            return accion_name, accion_values

class state_decorator(State):
    def _last_state_eq_new_state(self, new_state):
        return self.state == new_state
    
    def change_status_condicional(self, new_state):
        """
            Se define la condicion para cambiar de status
        """
        return (
            new_state >= self.state and 
            new_state - 1 == self.state # Esta condicion solo permite que 
            # se cante el TRUCO en primer lugar, RETRUCO en segunda y 
            # VALE 4 en tercera.
        )

class truco_handler(state_decorator):
    _game_instance = None
    _history : list = []
    _first_player : Jugador = None
    _quiero_team : Team = None # Indica cual es equipo que puede volver a cantar
    _active : bool = False # Indica si alguien canto bingo.
    _points : int = 1 # Indica la cantidad de puntos sumados en el truco.
    _last_chant : int = 0 # Indica cual es el ultimo usuario en cantar.
    _loop_envido : bool = False # Inidica nos encontramos en el loop de envido.
    _end_state = STATE_FINALIZADO
    
    def __init__(self, gameInstance):
        self._game_instance = gameInstance
        self._actions_map = {
            "truco": self.truco_handler,
            "retruco": self.retruco_handler,
            "value_4": self.vale4_handler,
            "quiero": self.quiero_handler
        }
    
    def _general_truco_logic(new_state):
        def decorator(func):
            def wrapper(*args):
                self = args[0]
                player = args[1]
                
                if self._last_state_eq_new_state(new_state):
                    raise ValueError("No podes volver a cantar")
                else:
                    if self.state != 0:
                        if self._quiero_team is not player.team:
                            raise ValueError("No podes cantar, tu oponente tiene el quiero")
                    self.state = new_state

                func(*args)

                next_player = self._game_instance.getTurnAndChange()
                accion_name, accion_values = get_response(
                    self._actions_map,
                    self._game_instance.signals_handler.getActionPlayer,
                    next_player, 
                    'truco'
                )

                self._actions_map[accion_name](next_player, accion_values)
                self._game_instance.getTurnAndChange()
            return wrapper
        return decorator

    @_general_truco_logic(STATE_TRUCO)
    def truco_handler(self, player: Jugador, *args):
        self._game_instance.signals_handler.showMessage(
            player, f"Jugador {player.getID()} canto truco"
        )
        self._points = 2

    @_general_truco_logic(STATE_RETRUCO)
    def retruco_handler(self, player: Jugador, *args):
        self._game_instance.signals_handler.showMessage(
            player, f"Jugador {player.getID()} canto retruco"
        )
        self._points = 3

    @_general_truco_logic(STATE_VALE_4)
    def vale4_handler(self, player: Jugador, *args):
        self._game_instance.signals_handler.showMessage(
            player, f"Jugador {player.getID()} canto vale 4"
        )
        self._points = 4
    

    def quiero_handler(self, player: Jugador, decision):
        if decision == SI:
            self._game_instance.signals_handler.showMessage(
                player, f"Jugador {player.getID()} quiso el truco"
            )
            self._quiero_team = player.team
        else:
            self._game_instance.signals_handler.showMessage(
                player, f"Jugador {player.getID()} no quiso el truco"
            )
            self._points -= 1
        
    
    def get_points(self):
        return self._points