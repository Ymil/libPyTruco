import sys
from cartas import Cartas
from accionesJuego import AccionesJuego
import logging
import inspect
import pdb
import time
import string
logging.basicConfig(format='%(levelname)s [%(asctime)s][SVR]: %(message)s',
    filename='./logs/libjuego.log', level='DEBUG')

global cuentaEjecucion
cuentaEjecucion = 0


def msg_debug(str1):
    global cuentaEjecucion
    # if(type(str1) is list):
    #    str1 = ' | '.join(tuple(list(str1))[0:])
    # print cuentaEjecucion
    str1 = 'EC %d' % cuentaEjecucion, str1
    # str1 = string.join(, ' ')
    #logging.debug(str1)
    cuentaEjecucion += 1

def msg_info(str1):
    global cuentaEjecucion
    # if(type(str1) is list):
    #    str1 = ' | '.join(tuple(list(str1))[0:])
    # print cuentaEjecucion
    str1 = 'EC %d' % cuentaEjecucion, str1
    # str1 = string.join(, ' ')
    #logging.info(str1)
    cuentaEjecucion += 1

class Game():
    ''' Clase controlador del Juego
    20-01-15 05:07AM Lautaro Linquiman'''
    def __init__(self, tableObject):
        self.status = 0
        self.tableObject = tableObject

        self.__loadVarsTheTable__()

        self.winningTeamFirstRound = 0# team ganador de la primera rond
        self.winningTeamSecondRound = 0
        # self.primerJugadorPartida = 0

        self.pardaObtenerGanador = 0

        self.hand = 0
        self.handNumber = 0
        self.turn = 0
        self.cards = Cartas()
        self.__envido = {}
        self.actionGame = AccionesJuego()
        self.resultLastHand = []  # Resultado de la ultima mano
        self.statusGame = 3
        ''' Esta variable almacena el estado actual del juego
        y es asignada por la funcion
        getResultHand [0:win|1:parda|2:empate|3:continue] '''

        self.lastCodeResult = 0
        '''Esta variable almacena un ID de la condicion verdadera al
        buscar un ganador'''

    def __loadVarsTheTable__(self):
        ''' Carga todas las variables necesarias de la mesa para poder iniciar el juego '''
        self.players = self.tableObject.getPlayers()
        self.teams = self.tableObject.getTeams()
        self.numberPlayers = len(self.players)# Obtiene la cantidad de jugadores

    def setActionGame(self, classActionGame):
        self.actionGame = classActionGame()

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def getTurn(self):
        ''' Obtiene el id del jugador que es mano
        @return{
            int
        } '''
        return self.turn
    def getTurnAndChange(self):
        ''' Obtiene el id del jugador que es hand y cambia la mano'''
        try:
            msg_debug('[getTurn-turn] %d' % self.turn)
        except:
            pdb.set_trace()
        if(self.turn == self.numberPlayers):
            self.turn = 0
        turn = self.players[self.turn]
        if self.getNumberTheCurrentHand == 0 and self.hand == 0:
            self.hand = self.turn
        self.changeTurn()
        return turn
    def changeTurn(self):
        ''' Cambia la hand del juego '''
        if(self.turn == self.numberPlayers):
            self.turn = 0
        else:
            self.turn += 1

    def setTurn(self, nListPlayer):
        '''Asigna el turno al jugador '''
        self.turn = self.players[nListPlayer]
        '''if(self.turn == self.numberPlayers):
            self.turn = 0'''
        #self.turn = self.turn

    def decCartaID(self, carta):
        ''' Valida que el valor ingresado por el jugador sea valido '''
        try:
            cardID = int(carta)
            if(cardID <= 3):
                return cardID-1
            else:
                return 20
        except ValueError:
            return 20

    def getRond(self):
        return self.handNumber

    def giveCardsToPlayers(self):
        ''' Se reparten las cartas de los jugadores '''
        self.cards.prepararMaso()
        for player in self.players:
                cardsPlayer = self.cards.repartir_individual()
                self.actionGame.giveCards(player.getID(), cardsPlayer)
                player.setCards(cardsPlayer)
                self.actionGame.showCards(player.getID(), cardsPlayer)

    '''def darCartas(self, playerID):
        self.playsCard[playerID] = []
        return self.cardPlayer[playerID]'''

    def giveCard(self, player, card):
        '''Asigna la carta jugada en la determinada ronda'''
        nrond = self.getRond()
        self.hands[nrond].append((player, card))

    def givePointsTeam(self, team, points):
        team.givePoints(points)

    def getPointsTeams(self):
        return self.teamPoints

    def getNumberTheCurrentHand(self):
        ''' Esta funcion duelve el numero de la mano actual '''
        self.numberTheCurrentHand = len(self.hands)
        return self.numberTheCurrentHand

    def getResultBeforeHand(self):
        ''' Devuelve el resultado de la mano anterior
        Solo se puede llamar despues de que se obtiene el resultado de una ronda
        y la mano es agregada en la variable hands
        return
        {
            'player': object Player,
            'parda': bool
        }
        '''
        numberThePreviusHand = self.getNumberTheCurrentHand()-1
        return self.hands[numberThePreviusHand]

    def getResultCurrentHand(self):
        '''Devuelve el ganador de la ultima mano
        return
        {
            'player': object Player,
            'parda': bool
        }
        '''

        numberTheCurrentHand = self.getNumberTheCurrentHand()

        tempResultHand = {'player': False, 'parda': False}
        # Resultado temporal de la mano
        for player in self.players:
            # No concuerda con la mano, falta terminar esto.

            try:
                tempCardWin = tempResultHand['player'].getCardTheNumberHand(\
                                        numberTheCurrentHand).getValue()
            except:
                '''Esta exception se captura cuando todavia no hay un jugador en
                el resultado ganador'''
                tempCardWin = 0
            playsCard = player.getCardTheNumberHand(numberTheCurrentHand).getValue()

            if tempCardWin < playsCard:
                tempResultHand['player'] = player
                tempResultHand['parda'] = False
            elif tempCardWin == playsCard:
                #Hay una parda
                tempResultHand['parda'] = True
        if tempResultHand['parda'] == True:
            self.statusGame = 1

        return tempResultHand

    def addResultHand(self, resultHand):
        ''' Agrega un resultado a la lista de manos '''
        self.hands.append(resultHand)

    def searchTeamWinnerTheRound(self):
        '''Esta funcion se ejecuta cuando se busca un equipo ganador
        de las rondas del juego
        @params
        null

        @return
        {
            'team': object Team or int 0 = no winner,
            'winner': int[1|0]
        }
        '''
        result = {'team': 0, 'winner': 0}
        msg_info("SearchTeamWinner")
        for team in self.teams:
            #pdb.set_trace()
            #Se recorren los equipos
            if team.getPoints() >= 30:
                msg_info("TeamWinner")
                #Un equipo tiene 30 o mas puntos
                result['team'] = team
                result['winner'] = 1
                msg_debug("TeamWinnerID:%d" % result['team'].getID())
        return result

    def getResultHandByNumber(self, numberHand):
        ''' Devuelve el resultado de una mano por su numero de mano '''
        return self.hands[numberHand]

    def getStatusTheRound(self):
        '''
            Esta funcion devuelve el resultado de la mano jugada y
            devuelve el estado que termino la mano
            @params
            null

            @return
            {
                'player': object Player,
                'parda': bool
            }
        '''
        tempResult = {}
        '''Devuelve este resultado cuando no existe un ganador pero si
        se captura un resultado'''
        resultCurrentHand = self.getResultCurrentHand()
        numberTheCurrentHand = self.getNumberTheCurrentHand()
        self.addResultHand(resultCurrentHand)
        if numberTheCurrentHand == 0:
            self.lastCodeResult = 0
            ''' En la primera mano se duelve el resultado sin ninguna comprobacion '''
            tempResult = resultCurrentHand
        elif numberTheCurrentHand > 0:
            numberThePreviusHand = numberTheCurrentHand-1
            winner = False
            if resultCurrentHand['parda'] and \
                    self.getResultHandByNumber(numberThePreviusHand)['parda']:
                self.lastCodeResult = 1
                msg_info(' En la mano actual y en la anterior ocurrio una parta:  \
                El Juego continua siempre y cuando esto ocurra en la segunda ronda  \
                En el caso de que esto ocurra en la tercera mano el jugador mano \
                de la primera mano es el ganador de la ronda')
                if numberTheCurrentHand != 1:
                    winner = self.getResultHandByNumber(0)
            elif not resultCurrentHand['parda'] and \
                    self.getResultHandByNumber(numberThePreviusHand)['parda']:
                self.lastCodeResult = 2
                msg_info(' En la mano anterior ocurrio una parda pero \
                en la mano actual no El ganador de la mano actual es \
                el ganador de la ronda')
                winner = resultCurrentHand
            elif resultCurrentHand['parda'] and \
                    not self.getResultHandByNumber(numberThePreviusHand)['parda']:
                self.lastCodeResult = 3
                msg_info(' En la mano anterior no hubo parda pero en la mano actual hay una parda \n \
                El jugador que gano la primera mano es el ganador de la ronda ')
                winner = self.getResultHandByNumber(0)
            elif resultCurrentHand['player'].getTeam() == \
                    self.getResultHandByNumber(numberThePreviusHand)['player'].getTeam():
                self.lastCodeResult = 4
                msg_info(' El Jugador que gana la mano actual es de \
                el mismo equipo que gano la mano anterior \
                El jugador de la mano actual es el ganador de la ronda')
                winner = self.getResultHandByNumber(numberTheCurrentHand)
            elif resultCurrentHand['player'].getTeam() !=  \
                    self.getResultHandByNumber(numberThePreviusHand)['player'].getTeam():
                self.lastCodeResult = 5
                msg_info(' C0: El jugador que gana la mano actual \
                no es del mismo equipo que gano la mano anterior  \
                El Juego continua siempre y cuando ocurra en la segunda mano \
                Si esto ocurre en la tercera mano se verifica si el ganador de\
                la mano es igual a el ganador de la primera mano')
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
            if winner != False:
                self.statusGame = 0
                return winner
        return tempResult

    def showPointsTeams(self):
        ''' Muestra los puntos de los equipos '''
        for team in self.teams:
            self.actionGame.showPoints(team.getID(), team.getPoints())
            #print ('points team %d: %d') %(team, self.teamPoints[team])

    ''' startEnvidoBlock '''
    def envido(self, player):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y inicia el loop de envido
        '''
        self.actionGame.envido(player)
        if len(self.__envido) == 0:
            self.playerChant = self.getTurn()
        self.__envido['player'] = player
        #pdb.set_trace()
        if not 'points' in self.__envido:
            self.__envido['points'] = 2
        else:
            self.__envido['points'] += 2

        if not self.__loopEnvido:
            self.loopEnvido()

    def loopEnvido(self):
        ''' Esta funcion se llama despues de que un jugador canta envido '''
        self.__loopEnvido = True
        while not 'winner' in self.__envido:
            player = self.getTurnAndChange()
            gameInfo = self.getInfo()
            accion = self.actionGame.getActionPlayer(\
                                player, gameInfo=gameInfo)
            if accion[0] == 'envido':
                self.envido(player)
            elif accion[0] == 'Quiero':
                if accion[1] == 1:
                    self.getWinnerEnvido()
                else:
                    self.actionGame.showWinnerEnvido(self.__envido['player'])
                    self.givePointsTeam(self.__envido['player'].getTeam(),2)

                self.__envido['winner'] = True
        pdb.set_trace()
    def getWinnerEnvido(self):
        ''' group: envido
        Esta funcion se llama cuando un jugador canta envido y otro lo acepta con un quiero
        '''
        winner = {'player': False}
        tempWinnerPoints = 0 #Esta variable almacena los puntos ganadores del envido
        cJugadas = 0
        self.setTurn(self.hand)
        while cJugadas < self.numberPlayers:
            cJugadas += 1
            player = self.getTurn()
            pPoints = player.getPointsEnvido()
            self.actionGame.showEnvido(player) #El jugador canta sus tantos
            if tempWinnerPoints < player.getPointsEnvido():
                winner = player
            tempWinnerPoints = player.getPointsEnvido()
        self.actionGame.showWinnerEnvido(winner)
        self.givePointsTeam(winner.getTeam(),2)
        try:
            self.setTurn(self.playerChant)
        except:
            pdb.set_trace()
    ''' endEnvidoBlock '''



    def start(self):
        self.actionGame.showMsgStartGame(self.players)
        self.actionGame.setPlayers(self.players)
        while 1:
            self.startRound()
            while not ( self.statusGame == 0 or self.statusGame == 2 ):
                #pdb.set_trace()
                self.startHand()

                cJugadas = 0 #Alamacena la cantidad de jugadas en la rond
                while cJugadas < self.numberPlayers:
                    '''Se inicia el juego'''
                    #pdb.set_trace()
                    cJugadas += 1
                    jugador = self.getTurnAndChange()

                    while 1:
                        while 1:
                            ''' Este loop obtiene la accion del jugador hasta que sea JugarCarta '''
                            gameInfo = self.getInfo()
                            accion = self.actionGame.getActionPlayer(\
                                                jugador, gameInfo=gameInfo)

                            if accion[0] == 'JugarCarta':
                                cartaAJugar = accion[1]
                                break
                            elif accion[0] == 'envido':
                                self.envido(jugador)
                                continue

                        if(1 == 1):
                            try:
                                if(jugador.playingCardInRound(cartaAJugar)):
                                    #Juega la carta y se comprueba que este disponible
                                    cartaJ = jugador.getNameCardPlayed()
                                    #Obitene el nombre completo de la carta
                                    #self.giveCard(jugador.getID(),cartaJ)
                                    self.actionGame.showCardPlaying(\
                                                    jugador.getTeam(), jugador,cartaJ)
                                    break
                                else:
                                    self.actionGame.showError(jugador.getID(),\
                                                            'cardPlayerd')
                            except:
                                pdb.set_trace()

                        else:
                            self.actionGame.showError(jugador.getID(), \
                                                        'invalidAction')
                self.finishHand()
            msg_info("EndRound")
            resultTheRound = self.finishRound()

            if resultTheRound['winner']:
                self.showPointsTeams()
                self.actionGame.winGameTeam(resultTheRound['team'])
                break
        self.actionGame.showMsgFinishGame()

    def getInfo(self):
        ''' Esta funcion devuelve un diccionario con informacion del juego
        @return
        {
            hand: int numero de mano actual
        }
        '''
        quiero = False if len(self.__envido) == 0 else True
        infoGame = {
            'hand': self.getNumberTheCurrentHand(),
            'quiero': quiero
        }

        return infoGame


    #eventos
    def startRound(self):
        ''' Esta funcion se llama cada vez que se inicia una nueva ronda
        @params: none
        @return: none
        '''
        self.resetRond()
        self.actionGame.showMsgStartRound()
        self.showPointsTeams()
        ''' Repartir cartas '''
        self.giveCardsToPlayers()
        self.hands = [] #Se resetea la variable hands

    def resetRond(self):
        ''' Esta funcion se llama cada vez se inicia una nueva ronda y vuelve a cargar todas las variables del juego'''
        self.__envido = {}
        self.hand = 0
        self.playerChant = 0 # Esta funcion alamacena al jugar que canta una jugada para volver a pararse en el al terminar el quiero
        self.__loopEnvido = False #Esta funcion indica si ya inicio el loop del envido
        self.handNumber = 0
        self.pardaObtenerGanador = 0
        self.statusGame = 3

    def finishRound(self):
        ''' finishround
        Esta funcion se ejecuta al terminar una ronda y se fija si alguno de
        los equipos tiene mas de 30 puntos para determinar un ganador
        @params: null

        @return
        {
            'team': object Team or int 0 = no winner,
            'winner': int[1|0]
        }
        '''
        self.actionGame.showMsgFinishRound()
        result = self.searchTeamWinnerTheRound()
        return result

    def startHand(self):
        ''' Esta funcion se llama cada vez que inicia una nueva ronda
        y se asigna el turno al jugador indicado '''
        self.handNumber += 1
        self.actionGame.showMsgStartHand(self.handNumber)
        #self.hand = self.getTurn()
        return self.handNumber

    def finishHand(self):
        ''' Esta funciona se llama cada vez que finaliza una ronda
        Analiza los datos del juego y determina si hay un ganador '''
        self.actionGame.showMsgFinishHand()
        msg_info("Iniciando analisis de resultados")
        Resultados = self.getStatusTheRound()
        self.actionGame.returnStatus(Resultados)
        #print Resultados
        msg_debug("lastCodeResult:%d" % self.lastCodeResult)
        if(self.statusGame == 1):
            self.actionGame.Parda()
            return
        RPlayer = Resultados['player']
        self.actionGame.showResultaTheHand(RPlayer.getID(),\
                            RPlayer.getName(),  RPlayer.getTeamID(),\
                            RPlayer.getNameCardPlayed())
        if(self.statusGame == 0):
            if(self.statusGame == 0):
                self.actionGame.win(Resultados['player'].getTeamID())
            elif(self.statusGame == 2):
                self.actionGame.winEmpate(\
                                    Resultados['player'].getTeamID())
            self.givePointsTeam(Resultados['player'].getTeam(),2)
