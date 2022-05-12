ENVIDO_SECUENCE = ["envido", "real_envido", "falta_envido"]
class envidoHandler:
    _gameInstance = None
    _history : list = []
    _playerChant : int = 0 # Indica quien fue el jugador que canto la primera ves.
    _active : bool = False # Indica si alguien canto bingo.
    _points : int = 0 # Indica la cantidad de puntos sumados en el envido.
    _lastChant : int = 0 # Indica cual es el ultimo usuario en cantar.
    _loopEnvido : bool = False # Inidica nos encontramos en el loop de envido.
    def __init__(self, gameInstance):
        self._gameInstance = gameInstance
    
    def _generalEnvidoLogic(self, playerObject, name: str):
        self._lastChant = playerObject
        if self._active:
            self_playerChant = self._gameInstance.getTurn()
        if not self._loopEnvido:
            self.loopEnvido()
        self._gameInstance.setTurn(self._gameInstance.playerChant) #Se le assigna el turno al jugador que canto el envido y continua el juego normalmente
        
    def envido(self, playerObject):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y inicia el loop de envido
        @param playerObject:
        '''
        self._points += 2
        self._gameInstance.actionGame.envido(playerObject)
        self._generalEnvidoLogic(playerObject, 'envido')
    
    def loopEnvido(self):
        ''' Esta funcion se llama despues de que un jugador canta envido '''
        self._gameInstance.actionGame.startLoopEnvido()
        self._loopEnvido = True
        while not 'winner' in self._gameInstance.e__envido:
            player = self._gameInstance.getTurnAndChange()
            gameInfo = self._gameInstance.getInfo()
            accion = self._gameInstance.actionGame.getActionPlayer(\
                                player, gameInfo=gameInfo)
            if accion[0] == 'envido':
                self.envido(player)
            elif accion[0] == 'Quiero':
                if accion[1] == 1:
                    self._gameInstance.actionGame.quiero(player)
                    self.getWinnerEnvido()
                else:
                    self._gameInstance.actionGame.noQuiero(player)
                    self._gameInstance.actionGame.showWinnerEnvido(self._lastChant)
                    self._gameInstance.givePointsTeam(self._lastChant.getTeam(), 2)

                # self._gameInstance.e__envido['winner'] = True
            #pdb.set_trace()
        self._gameInstance.actionGame.finishLoopEnvido()

        #pdb.set_trace()
    def getWinnerEnvido(self):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y otro lo acepta con un quiero
        '''
        winner = {'player': False}
        tempWinnerPoints = 0 #Esta variable almacena los puntos ganadores del envido
        cJugadas = 0
        self._gameInstance.setTurn(self._gameInstance.hand)
        while cJugadas < self._gameInstance.numberPlayers:
            cJugadas += 1
            player = self._gameInstance.getTurnAndChange()
            pPoints = player.getPointsEnvido()
            self._gameInstance.actionGame.showEnvido(player) #El jugador canta sus tantos
            if tempWinnerPoints < player.getPointsEnvido():
                winner = player
            tempWinnerPoints = player.getPointsEnvido()
        self._gameInstance.actionGame.showWinnerEnvido(winner)
        self._gameInstance.givePointsTeam(winner.getTeam(), self._points) #Se le asigna los puntos del envido al equipo ganador