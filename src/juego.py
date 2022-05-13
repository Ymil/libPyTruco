#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-
__author__ = "Lautaro Linquiman"
__email__ = "acc.limayyo@gmail.com"
__status__ = "Developing"
__data__ = "20-01-15 05:07AM"



import sys
from cartas import Cartas
from envido_handler import envido_handler
from truco_handler import truco_handler
import logging
import inspect
import pdb
import time
import string


global cuentaEjecucion
cuentaEjecucion = 0



def msg_debug(str1):
    global cuentaEjecucion
    # if(type(str1) is list):
    #    str1 = ' | '.join(tuple(list(str1))[0:])
    # print(cuentaEjecucion)
    str1 = 'EC %d' % cuentaEjecucion, str1
    # str1 = string.join(, ' ')
    #logging.debug(str1)
    cuentaEjecucion += 1

def msg_info(str1):
    global cuentaEjecucion
    # if(type(str1) is list):
    #    str1 = ' | '.join(tuple(list(str1))[0:])
    # print(cuentaEjecucion)
    str1 = 'EC %d' % cuentaEjecucion, str1
    # str1 = string.join(, ' ')
    #logging.info(str1)
    cuentaEjecucion += 1

class Game():
    def __init__(self, tableObject, signalsHandler, configGame = {}):
        '''
        @param tableObject:
        @param configGame: dic
        '''
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
        self.e__envido = {}
        self.signals_handler = signalsHandler
        self.resultLastHand = []  # Resultado de la ultima mano
        self.resultLast = [] #Almacena los ultimos rezultados de la func
        self.statusGame = 3
        self.pointsByWin = configGame['pointsByWin'] if 'pointsByWin' in configGame else 30
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
        # self._envidoHandler = envido_handler(self)
        # self._truco_handler = truco_handler(self)

    def setActionGame(self, classActionGame):
        ''' Se asigna otra objecto classActionGame
        @param classActionGame:  '''
        self.signals_handler = classActionGame()

    def getStatus(self):
        '''
        @return: Estado del juego
        @rtype: int '''
        return self.status

    def setStatus(self, status):
        ''' Se asgina una estado de juego
        @param status: int '''
        self.status = status

    def getTurn(self):
        '''
        @return: el numero de turno que toca jugar
        @rtype: int'''
        return self.turn

    def getNextTurn(self, player):
        nextTurn = self.players.index(player) + 1
        if(nextTurn >= self.numberPlayers):
            return self.players[0]
        return self.players[nextTurn]

    def getTurnAndChange(self):
        ''' Obtiene el id del jugador que es hand y cambia la mano
        @rtype: playerObject'''
        # msg_debug('[getTurn-turn] %d' % self.turn)
        turn = self.players[self.turn]
        if self.getNumberTheCurrentHand == 0 and self.hand == 0:
            self.hand = self.turn
        self.changeTurn()
        return turn

    def changeTurn(self):
        ''' Cambia la hand del juego '''
        self.turn += 1
        if(self.turn >= self.numberPlayers):
            self.turn = 0
        #else:


    def setTurn(self, nListPlayer):
        '''Asigna el turno al jugador
        @param nListPlayer: int'''
        self.turn = nListPlayer
        '''if(self.turn == self.numberPlayers):
            self.turn = 0'''
        #self.turn = self.turn

    def decCartaID(self, carta):
        ''' Valida que el valor ingresado por el jugador sea valido
        @param carta:
        @rtype: int'''
        try:
            cardID = int(carta)
            if(cardID <= 3):
                return cardID-1
            else:
                return 20
        except ValueError:
            return 20

    def getRond(self):
        '''
        @return: Deuelve el numero de la mano
        @rtype: int '''
        return self.handNumber

    def giveCardsToPlayers(self):
        ''' Se reparten las cartas de los jugadores '''
        self.cards.prepararMaso()
        for player in self.players:
                cardsPlayer = self.cards.repartir_individual()
                self.signals_handler.giveCards(player.getID(), cardsPlayer)
                player.setCards(cardsPlayer)
                self.signals_handler.showCards(player, cardsPlayer)

    '''def darCartas(self, playerID):
        self.playsCard[playerID] = []
        return self.cardPlayer[playerID]'''

    def giveCard(self, playerObject, cardObject):
        '''Asigna las carta jugadas en la determinada ronda
        @param playerObject:
        @param cardObject:'''
        nrond = self.getRond()
        self.hands[nrond].append((playerObject, cardObject))

    def givePointsTeam(self, teamObject, points):
        '''Le suma punto a un equipo
        @param teamObject:
        @param points: int'''
        teamObject.givePoints(points)

    def getPointsTeams(self):
        ''' obsoleto ? '''
        return self.teamPoints

    def getNumberTheCurrentHand(self):
        ''' Esta funcion duelve el
        @return: numero de la mano actual
        @rtype: int '''
        self.numberTheCurrentHand = len(self.hands)
        return self.numberTheCurrentHand

    def getResultBeforeHand(self):
        ''' Devuelve el resultado de la mano anterior
        Solo se puede llamar despues de que se obtiene el resultado de una ronda
        y la mano es agregada en la variable hands
        @return: {player: playerObject, parda: bool}
        @rtype: dic
        '''
        numberThePreviusHand = self.getNumberTheCurrentHand()-1
        return self.hands[numberThePreviusHand]

    def getResultCurrentHand(self):
        '''Devuelve el ganador de la ultima mano
        @return: {player: playerObject, parda: bool}
        @rtype: dic
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
            #pdb.set_trace()
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
        ''' Agrega un resultado a la lista de manos
        @param resultHand:'''
        self.hands.append(resultHand)

    def searchTeamWinnerTheRound(self):
        '''Esta funcion se ejecuta cuando se busca un
        @return: equipo ganador de las rondas del juego {'team': object Team, 'winner': int[1|0]}
        @rtype: dic
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
        ''' Devuelve el resultado de una mano por su numero de mano
        @param numberHand: int
        @return: {player: playerObject, parda: bool}
        @rtype: dic'''
        return self.hands[numberHand]

    def getStatusTheRound(self):
        '''
        Esta funcion devuelve el resultado de la mano jugada y
        devuelve el estado que termino la mano
        @return: {player: playerObject, parda: bool}
        @rtype: dic

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
            self.signals_handler.showPoints(team.getID(), team.getPoints())
            #print(('points team %d: %d') %(team, self.teamPoints[team]))

    def playingCardInRound(self, player, card):
        if(player.playingCardInRound(card)):
            #Juega la carta y se comprueba que este disponible
            cartaJ = player.getNameCardPlayed()
            #Obitene el nombre completo de la carta
            #self.giveCard(jugador.getID(),cartaJ)
            self.signals_handler.showCardPlaying(\
                            player.getTeam(), player,cartaJ)
            self.CHANGE_TURN_FLAG = True
        else:
            self.signals_handler.showError(player,\
                                    'cardPlayerd')
    CHANGE_TURN_FLAG = False
    def start(self):
        ''' Esta funcion se llama cuando se inicia el juego '''
    
        self.signals_handler.showMsgStartGame(self.players)
        self.signals_handler.setPlayers(self.players)
        while 1:
            self.startRound()
            _actions_map : dict = {
                "envido": self._envidoHandler.envido_handler,
                "real_envido": self._envidoHandler.real_envido_handler,
                "falta_envido": self._envidoHandler.falta_envido_handler,
                "truco": self._truco_handler.truco_handler,
                "retruco": self._truco_handler.retruco_handler,
                "value_4": self._truco_handler.vale4_handler,
                "jugarCarta": self.playingCardInRound
            }
            while not ( self.statusGame == 0 or self.statusGame == 2 ):
                #pdb.set_trace()
                self.startHand()

                cJugadas = 0 #Alamacena la cantidad de jugadas en la rond
                # while cJugadas < self.numberPlayers:
                for _ in self.players:
                    self.CHANGE_TURN_FLAG = False
                    '''Se inicia el juego'''
                    #pdb.set_trace()
                    # cJugadas += 1
                    jugador = self.getTurnAndChange()

                    while not self.CHANGE_TURN_FLAG:
                        ''' Este loop obtiene la accion del jugador hasta que sea jugarCarta '''
                        gameInfo = self.getInfo()

                        accion_name, accion_value = self.signals_handler.getActionPlayer(\
                                            jugador)

                        try:
                            if accion_name in _actions_map:
                                _actions_map[accion_name](jugador, accion_value)
                        except ValueError as msg:
                            self.signals_handler.showError(jugador,\
                                                        msg)
                self.finishHand()
            msg_info("EndRound")
            resultTheRound = self.finishRound()

            if resultTheRound['winner']:
                self.showPointsTeams()
                self.signals_handler.winGameTeam(resultTheRound['team'])
                break
        self.signals_handler.showMsgFinishGame()

    def getInfo(self):
        ''' Esta funcion devuelve un diccionario con informacion del juego
        @return: { hand: int numero de mano actual, envido: {}}
        @rtype: dic
        '''
        #quiero = False if len(self.e__envido) == 0 or 'winner' in self.e__envido else True
        infoGame = {
            'hand': self.getNumberTheCurrentHand(),
            'envido': self.e__envido
        }

        return infoGame


    #eventos
    def startRound(self):
        ''' Esta funcion se llama cada vez que se inicia una nueva ronda
        '''
        self.resetRond()
        self.signals_handler.showMsgStartRound()
        self.showPointsTeams()
        ''' Repartir cartas '''
        self.giveCardsToPlayers()
        self.hands = [] #Se resetea la variable hands

    def resetRond(self):
        ''' Esta funcion se llama cada vez se inicia una nueva ronda y vuelve a cargar todas las variables del juego'''
        self.e__envido = {}
        self.hand = 0
        self.playerChant = 0 # Esta funcion alamacena al jugar que canta una jugada para volver a pararse en el al terminar el quiero
        self.handNumber = 0
        self.pardaObtenerGanador = 0
        self.statusGame = 3
        self._envidoHandler = envido_handler(self)
        self._truco_handler = truco_handler(self)

    def finishRound(self):
        ''' Esta funcion se ejecuta al terminar una ronda y se fija si alguno de
        los equipos tiene mas de 30 puntos para determinar un ganador

        @return: {'team': objectTeam , 'winner': int[1|0]}
        @rtype: dic

        '''
        self.signals_handler.showMsgFinishRound()
        result = self.searchTeamWinnerTheRound()
        return result

    def startHand(self):
        ''' Esta funcion se llama cada vez que inicia una nueva ronda
        y se asigna el turno al jugador indicado
        @return: Numero de la mano que se va iniciar
        @rtype: int
         '''
        self.handNumber += 1
        self.signals_handler.showMsgStartHand(self.handNumber)
        #self.hand = self.getTurn()
        return self.handNumber

    def finishHand(self):
        ''' Esta funciona se llama cada vez que finaliza una ronda
        Analiza los datos del juego y determina si hay un ganador '''
        self.signals_handler.showMsgFinishHand()
        msg_info("Iniciando analisis de resultados")
        self.resultLastHand = self.getStatusTheRound()
        Resultados = self.resultLastHand
        self.signals_handler.returnStatus(Resultados)
        #print(Resultados)
        msg_debug("lastCodeResult:%d" % self.lastCodeResult)
        if(self.statusGame == 1):
            self.signals_handler.Parda()
            return

        RPlayer = Resultados['player']
        self.signals_handler.showResultaTheHand(RPlayer.getID(),\
                            RPlayer.getName(),  RPlayer.getTeamID(),\
                            RPlayer.getNameCardPlayed())
        if(self.statusGame == 0):
            if(self.statusGame == 0):
                self.signals_handler.win(Resultados['player'].getTeamID())
            elif(self.statusGame == 2):
                self.signals_handler.winEmpate(\
                                    Resultados['player'].getTeamID())
            self.givePointsTeam(
                Resultados['player'].getTeam(),
                self._truco_handler.get_points() # Se obtienen los puntos del truco en caso de existir
            )
