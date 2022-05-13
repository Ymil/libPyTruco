from state import State

ENVIDO_SECUENCE = ["envido", "real_envido", "falta_envido"]
STATE_ENVIDO = 1
STATE_REAL_ENVIDO = 2
STATE_FALTA_ENVIDO = 3
STATE_FINALIZADO = 4

SI = 1
NO = 0
class envido_handler(State):
    _game_instance = None
    _history : list = []
    _player_chant : int = None # Indica quien fue el jugador que canto la primera ves.
    _active : bool = False # Indica si alguien canto envido.
    _points : int = 0 # Indica la cantidad de puntos sumados en el envido.
    _last_chant : int = 0 # Indica cual es el ultimo usuario en cantar.
    _loop_envido : bool = False # Inidica nos encontramos en el loop de envido.
    def __init__(self, gameInstance):
        self._game_instance = gameInstance
        self._actions_map : dict = {
            "envido": self.envido_handler,
            "real_envido": self.real_envido_handler,
            "falta_envido": self.falta_envido_handler,
            "quiero": self.quiero_handler
        }
    
    def _general_envido_logic(new_state):
        def decorator(func):
            def wrapper(*args):
                self = args[0]
                player = args[1]
                self.state = new_state
                if self._game_instance._truco_handler.state > 0:
                    raise ValueError("No puedes cantar envido despues del truco")
                if self._game_instance.handNumber != 1:
                    raise ValueError("No podes cantar envido en esta mano")
                
                func(*args)

                self._game_instance.actionGame.envido(player)
                self._last_chant = player
                if self._player_chant == None:
                    self._player_chant = self._game_instance.getTurn()
                if not self._loop_envido:
                    self.loopEnvido()
                self._game_instance.setTurn(self._player_chant) #Se le assigna el turno al jugador que canto el envido y continua el juego normalmente
            return wrapper
        return decorator
    
    @_general_envido_logic(STATE_ENVIDO)
    def envido_handler(self, player, *args):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y inicia el loop de envido
        @param player:
        '''
        self._points += 2
        
    
    @_general_envido_logic(STATE_REAL_ENVIDO)
    def real_envido_handler(self, player, *args):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y inicia el loop de envido
        @param player:
        '''
        self._points += 3
    
    @_general_envido_logic(STATE_FALTA_ENVIDO)
    def falta_envido_handler(self, player, *args):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y inicia el loop de envido
        @param player:
        '''
        self._points += 15
    
    def quiero_handler(self, player, decision):
        if decision == SI:
            self._game_instance.actionGame.quiero(player)
            self.getWinnerEnvido()
        else:
            self._game_instance.actionGame.noquiero(player)
            self._game_instance.actionGame.showWinnerEnvido(self._last_chant)
            self._game_instance.givePointsTeam(self._last_chant.getTeam(), 2)
        self.state = STATE_FINALIZADO

    
    def loopEnvido(self):
        ''' Esta funcion se llama despues de que un jugador canta envido '''
        self._game_instance.actionGame.startLoopEnvido()
        self._loop_envido = True
        while (self.state is not STATE_FINALIZADO):
            player = self._game_instance.getTurnAndChange()
            accion_name, accion_values = self._game_instance.actionGame.getActionPlayer(\
                                player, action='envido')

            if accion_name in self._actions_map:
                self._actions_map[accion_name](player, accion_values)

        self._game_instance.actionGame.finishLoopEnvido()
        

    def getWinnerEnvido(self):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y otro lo acepta con un quiero
        '''
        winner = {'player': False}
        tempWinnerPoints = 0 #Esta variable almacena los puntos ganadores del envido
        cJugadas = 0
        self._game_instance.setTurn(self._game_instance.hand)
        while cJugadas < self._game_instance.numberPlayers:
            cJugadas += 1
            player = self._game_instance.getTurnAndChange()
            pPoints = player.getPointsEnvido()
            self._game_instance.actionGame.showEnvido(player) #El jugador canta sus tantos
            if tempWinnerPoints < player.getPointsEnvido():
                winner = player
            tempWinnerPoints = player.getPointsEnvido()
        self._game_instance.actionGame.showWinnerEnvido(winner)
        self._game_instance.givePointsTeam(
            winner.getTeam(), self._points
        ) #Se le asigna los puntos del envido al equipo ganador