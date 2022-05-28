from .cartas import Cartas
from .envido_handler import envido_handler
from .handlers.turn import TurnHandler
from .truco_handler import truco_handler, TrucoNoQuerido
from .handlers.signals import signals
from .utils import get_response

class Game():
    def __init__(self, table, configGame={}):
        '''
        :param tableObject:
        :param configGame: dic
        '''
        self.status = 0
        self.table = table

        self.__loadVarsTheTable__()

        self.pardaObtenerGanador = 0

        self.hand = 0
        self.handNumber = 0
        self.turn = 0
        self.cards = Cartas()
        self.e__envido = {}
        self.resultLastHand = []  # Resultado de la ultima mano
        self.resultLast = []  # Almacena los ultimos rezultados de la func
        self.statusGame = 3
        self.pointsByWin = 30
        ''' Esta variable almacena el estado actual del juego
        y es asignada por la funcion
        getResultHand [0:win|1:parda|2:empate|3:continue] '''

        self.lastCodeResult = 0
        '''Esta variable almacena un ID de la condicion verdadera al
        buscar un ganador'''

    def __loadVarsTheTable__(self):
        ''' Carga todas las variables necesarias de la mesa
        para poder iniciar el juego '''
        self.players = self.table.getPlayers()
        self.turn_handler = TurnHandler(self.players)
        self.teams = self.table.getTeams()
        self.numberPlayers = len(self.players)

    def getNextTurn(self, player):
        nextTurn = self.players.index(player) + 1
        if(nextTurn >= self.numberPlayers):
            return self.players[0]
        return self.players[nextTurn]

    def getRond(self):
        '''

        :return: Deuelve el numero de la mano
        :rtype: int '''
        return self.handNumber

    def giveCardsToPlayers(self):
        ''' Se reparten las cartas de los jugadores '''
        self.cards.prepararMaso()
        for player in self.players:
            cardsPlayer = self.cards.repartir_individual()
            self.table.signals_handler.giveCards(player.getID(), cardsPlayer)
            player.setCards(cardsPlayer)
            self.table.signals_handler.showCards(player, cardsPlayer)

    def giveCard(self, playerObject, cardObject):
        '''Asigna las carta jugadas en la determinada ronda

        :param playerObject:
        :param cardObject:'''
        nrond = self.getRond()
        self.hands[nrond].append((playerObject, cardObject))

    def givePointsTeam(self, teamObject, points):
        '''Le suma punto a un equipo

        :param teamObject:
        :param points: int'''
        teamObject.givePoints(points)

    def getNumberTheCurrentHand(self):
        ''' Esta funcion duelve el

        :return: numero de la mano actual
        :rtype: int '''
        self.numberTheCurrentHand = len(self.hands)
        return self.numberTheCurrentHand

    def getResultBeforeHand(self):
        ''' Devuelve el resultado de la mano anterior
        Solo se puede llamar despues de que se obtiene el
         resultado de una ronda
        y la mano es agregada en la variable hands

        :return: {player: playerObject, parda: bool}
        :rtype: dic
        '''
        numberThePreviusHand = self.getNumberTheCurrentHand()-1
        return self.hands[numberThePreviusHand]

    def addResultHand(self, resultHand):
        ''' Agrega un resultado a la lista de manos

        :param resultHand:'''
        self.hands.append(resultHand)

    def searchTeamWinnerTheRound(self):
        '''Esta funcion se ejecuta cuando se busca un

        :return: equipo ganador de las rondas del juego
            {'team': object Team, 'winner': int[1|0]}
        :rtype: dic
        '''
        result = {'team': 0, 'winner': 0}
        for team in self.teams:
            # Se recorren los equipos
            if team.getPoints() >= 30:
                # Un equipo tiene 30 o mas puntos
                result['team'] = team
                result['winner'] = 1
        return result

    def getResultHandByNumber(self, numberHand):
        ''' Devuelve el resultado de una mano por su numero de mano

        :param numberHand: int        
        :return: {player: playerObject, parda: bool}
        :rtype: dic'''
        return self.hands[numberHand]

    def getResultCurrentHand(self):
        '''Devuelve el ganador de la ultima mano

        :return: {player: playerObject, parda: bool}
        :rtype: dic
        '''

        numberTheCurrentHand = self.getNumberTheCurrentHand()

        tempResultHand = {
            'player': None,
            'parda': False,
        }
        # Resultado temporal de la mano
        for player in self.players:
            # No concuerda con la mano, falta terminar esto.

            if tempResultHand['player'] is not None:
                tempCardWin = tempResultHand['player'].getCardTheNumberHand(
                    numberTheCurrentHand,
                ).getValue()
            else:
                '''Esta exception se captura cuando todavia
                no hay un jugador en
                el resultado ganador'''
                tempCardWin = 0
            # pdb.set_trace()
            playsCard = player.getCardTheNumberHand(
                numberTheCurrentHand,
            ).getValue()

            if tempCardWin < playsCard:
                tempResultHand['player'] = player
                tempResultHand['parda'] = False
            elif tempCardWin == playsCard:
                # Hay una parda
                tempResultHand['parda'] = True
        if tempResultHand['parda'] is True:
            self.statusGame = 1

        return tempResultHand

    def getStatusTheRound(self):
        '''
        Esta funcion devuelve el resultado de la mano jugada y
        devuelve el estado que termino la mano

        :return: {player: playerObject, parda: bool}
        :rtype: dic

        '''
        tempResult = {}
        '''Devuelve este resultado cuando no existe un ganador pero si
        se captura un resultado'''
        resultCurrentHand = self.getResultCurrentHand()
        if resultCurrentHand['player'] is not None:
            self.turn_handler.change_hand(resultCurrentHand['player'])
        numberTheCurrentHand = self.getNumberTheCurrentHand()
        self.addResultHand(resultCurrentHand)
        if numberTheCurrentHand == 0:
            self.lastCodeResult = 0
            ''' En la primera mano se duelve el resultado
             sin ninguna comprobacion '''
            tempResult = resultCurrentHand
        elif numberTheCurrentHand > 0:
            numberThePreviusHand = numberTheCurrentHand-1
            winner = False
            if resultCurrentHand['parda'] and \
                    self.getResultHandByNumber(numberThePreviusHand)['parda']:
                self.lastCodeResult = 1
                ''' En la mano actual y en \
                     la anterior ocurrio una parta:  \
                El Juego continua siempre y \
                     cuando esto ocurra en la segunda ronda  \
                En el caso de que esto ocurra \
                     en la tercera mano el jugador mano \
                de la primera mano es el ganador de la ronda'''
                if numberTheCurrentHand != 1:
                    winner = self.getResultHandByNumber(0)
            elif not resultCurrentHand['parda'] and \
                    self.getResultHandByNumber(
                        numberThePreviusHand,
                    )['parda']:
                self.lastCodeResult = 2
                ''' En la mano anterior ocurrio una parda pero
                en la mano actual no El ganador de la mano actual es
                el ganador de la ronda'''
                winner = resultCurrentHand
            elif resultCurrentHand['parda'] and \
                    not self.getResultHandByNumber(
                        numberThePreviusHand,
                    )['parda']:
                self.lastCodeResult = 3
                ''' En la mano anterior no hubo parda pero en la mano
                 actual hay una parda \n 
                El jugador que gano la primera mano es el ganador de la 
                    ronda '''
                winner = self.getResultHandByNumber(0)
            elif resultCurrentHand['player'].getTeam() == \
                    self.getResultHandByNumber(
                        numberThePreviusHand,
                    )['player'].getTeam():
                self.lastCodeResult = 4
                ''' El Jugador que gana la mano actual es de
                el mismo equipo que gano la mano anterior
                El jugador de la mano actual es el ganador de la ronda'''
                winner = self.getResultHandByNumber(numberTheCurrentHand)
            elif resultCurrentHand['player'].getTeam() !=  \
                    self.getResultHandByNumber(
                        numberThePreviusHand,
                    )['player'].getTeam():
                self.lastCodeResult = 5
                ''' C0: El jugador que gana la mano actual
                no es del mismo equipo que gano la mano anterior 
                El Juego continua siempre y cuando ocurra en la segunda mano
                Si esto ocurre en la tercera mano se verifica si el ganador d
                la mano es igual a el ganador de la primera mano'''
                if numberTheCurrentHand == 1:
                    self.statusGame = 3
                    tempResult = self.getResultHandByNumber(1)
                elif numberTheCurrentHand == 2:
                    if resultCurrentHand['player'].getTeam() == \
                            self.getResultHandByNumber(0)['player'].getTeam():
                        winner = self.getResultHandByNumber(0)
                    elif resultCurrentHand['player'].getTeam() == \
                            self.getResultHandByNumber(1)['player'].getTeam():
                        winner = self.getResultHandByNumber(1)
            if winner is not False:
                self.statusGame = 0
                return winner
        return tempResult

    def showPointsTeams(self):
        ''' Muestra los puntos de los equipos '''
        for team in self.teams:
            self.table.signals_handler.show_points_for_team(
                team.getID(), team.getPoints(),
            )

    def playingCardInRound(self, player, card):
        if(player.playingCardInRound(card)):
            # Juega la carta y se comprueba que este disponible
            cartaJ = player.getNameCardPlayed()
            # Obitene el nombre completo de la carta
            self.table.signals_handler.showCardPlaying(
                player.getTeam(), player, cartaJ,
            )
            self.CHANGE_TURN_FLAG = True
        else:
            self.table.signals_handler.showError(
                player,
                'cardPlayerd',
            )
    CHANGE_TURN_FLAG = False

    def start(self):
        ''' Esta funcion se llama cuando se inicia el juego '''

        self.table.signals_handler.showMsgStartGame()
        while 1:
            self.startRound()
            _actions_map: dict = {
                'envido': self._envidoHandler.envido_handler,
                'real_envido': self._envidoHandler.real_envido_handler,
                'falta_envido': self._envidoHandler.falta_envido_handler,
                'truco': self._truco_handler.truco_handler,
                'retruco': self._truco_handler.retruco_handler,
                'value_4': self._truco_handler.vale4_handler,
                'jugarCarta': self.playingCardInRound,
            }
            while not (self.statusGame == 0 or self.statusGame == 2):
                self.startHand()

                try:
                    for player in self.turn_handler:
                        self.CHANGE_TURN_FLAG = False
                        '''Se inicia el juego'''

                        while not self.CHANGE_TURN_FLAG:
                            ''' Este loop obtiene la accion del
                                jugador hasta que sea jugarCarta '''
                            accion_name, accion_value = get_response(
                                _actions_map,
                                self.table.signals_handler.getActionPlayer,
                                player,
                            )
                            try:
                                if accion_name in _actions_map:
                                    _actions_map[accion_name](
                                        player, accion_value,
                                    )
                            except ValueError as msg:
                                self.table.signals_handler.showError(
                                    player,
                                    msg,
                                )
                except TrucoNoQuerido as e:
                    self.finishHand(e.winPlayer)
                    break

                self.finishHand()
            resultTheRound = self.finishRound()

            if resultTheRound['winner']:
                self.showPointsTeams()
                self.table.signals_handler.winGameTeam(resultTheRound['team'])
                break
        self.table.signals_handler.showMsgFinishGame()

    def getInfo(self):
        ''' Esta funcion devuelve un diccionario con informacion del juego

        :return: { hand: int numero de mano actual, envido: {}}
        :rtype: dic
        '''
        infoGame = {
            'hand': self.getNumberTheCurrentHand(),
            'envido': self.e__envido,
        }

        return infoGame

    # eventos

    def startRound(self):
        ''' Esta funcion se llama cada vez que se inicia una nueva ronda
        '''
        self.resetRond()
        self.table.signals_handler.start_new_round()
        self.showPointsTeams()
        ''' Repartir cartas '''
        self.giveCardsToPlayers()
        self.hands = []  # Se resetea la variable hands

    def resetRond(self):
        ''' Esta funcion se llama cada vez se inicia una nueva ronda y
            vuelve a cargar todas las variables del juego'''
        self.e__envido = {}
        self.hand = 0
        self.handNumber = 0
        self.pardaObtenerGanador = 0
        self.statusGame = 3
        self._envidoHandler = envido_handler(self)
        self._truco_handler = truco_handler(self)

    def finishRound(self):
        ''' Esta funcion se ejecuta al terminar una ronda y se fija si alguno
        de
        los equipos tiene mas de 30 puntos para determinar un ganador

        :return: {'team': objectTeam , 'winner': int[1|0]}
        :rtype: dic

        '''
        self.table.signals_handler.showMsgFinishRound()
        self.turn_handler.change_round()
        result = self.searchTeamWinnerTheRound()
        return result

    def startHand(self):
        ''' Esta funcion se llama cada vez que inicia una nueva ronda
        y se asigna el turno al jugador indicado

        :return: Numero de la mano que se va iniciar
        :rtype: int
         '''
        self.handNumber += 1
        self.table.signals_handler.start_new_hand(self.handNumber)
        return self.handNumber

    def finishHand(self, winner=None):
        ''' Esta funciona se llama cada vez que finaliza una ronda
        Analiza los datos del juego y determina si hay un ganador '''
        self.table.signals_handler.showMsgFinishHand()
        if winner is None:
            self.resultLastHand = self.getStatusTheRound()
            Resultados = self.resultLastHand
        else:
            Resultados = {
                'player': winner,
            }
            self.statusGame = 0
        self.table.signals_handler.returnStatus(Resultados)
        if(self.statusGame == 1):
            self.table.signals_handler.Parda()
            return

        RPlayer = Resultados['player']
        self.table.signals_handler.showResultaTheHand(
            RPlayer.getID(),
            RPlayer.getName(),  RPlayer.getTeamID(),
            RPlayer.getNameCardPlayed(),
        )
        if(self.statusGame == 0):
            if(self.statusGame == 0):
                self.table.signals_handler.win(Resultados['player'].getTeamID())
            elif(self.statusGame == 2):
                self.table.signals_handler.winEmpate(
                    Resultados['player'].getTeamID(),
                )

            Resultados['player'].getTeam().givePoints(
                self._truco_handler.get_points()
            )