import sys
from cartas import Cartas
from accionesJuego import AccionesJuego
import logging
import inspect
import pdb
import time
import string
logging.basicConfig(format='%(levelname)s [%(asctime)s][SVR]: %(message)s',
    filename='./logs/libjuego.log', level='INFO')

global cuentaEjecucion
cuentaEjecucion = 0


def msg_debug(str1):
    global cuentaEjecucion
    # if(type(str1) is list):
    #    str1 = ' | '.join(tuple(list(str1))[0:])
    # print cuentaEjecucion
    str1 = 'EC %d' % cuentaEjecucion, str1
    # str1 = string.join(, ' ')
    logging.debug(str1)
    cuentaEjecucion += 1

def msg_info(str1):
    global cuentaEjecucion
    # if(type(str1) is list):
    #    str1 = ' | '.join(tuple(list(str1))[0:])
    # print cuentaEjecucion
    str1 = 'EC %d' % cuentaEjecucion, str1
    # str1 = string.join(, ' ')
    logging.info(str1)
    cuentaEjecucion += 1

class Game():
    ''' Clase controlador del Juego
    20-01-15 05:07 Lautaro Linquiman'''
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
        self.cards = Cartas(self.numberPlayers, 0)
        self.actionGame = AccionesJuego()
        self.resultLastHand = []  # Resultado de la ultima mano
        self.statusGame = 3# Esta variable almacena el estado actual del juego y es asignada por la funcion getResultHand [0:win|1:parda|2:empate|3:continue]

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
        ''' Obtiene el id del jugador que es hand '''
        msg_debug('[getTurn-turn] %d' % self.turn)
        if(self.turn == self.numberPlayers):
            self.turn = 0
        turn = self.players[self.turn]
        self.changeTurn()
        return turn

    def changeTurn(self):
        ''' Cambia la hand del juego '''
        if(self.turn == self.numberPlayers):
            self.turn = 0
        else:
            self.turn += 1

    def setTurn(self, playerID):
        '''Asigna el turno al jugador '''
        self.turn = self.players[playerID].getID()
        if(self.turn == self.numberPlayers):
            self.turn = 0
        self.turn = self.turn

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

    def startHand(self):
        ''' Se inicia la una nueva ronda y se asigna el turno al
        jugador indicado '''
        self.handNumber += 1
        #self.hand = self.getTurn()
        return self.handNumber

    def resetRond(self):
        self.handNumber = 0
        self.pardaObtenerGanador = 0

    def getRond(self):
        return self.handNumber

    def giveCardsToPlayers(self):
        ''' Se reparten las cartas de los jugadores '''

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

    def getResultPreviousHand(self):
        ''' Devuelve el resultado de la mano anterior
        Solo se puede llamar despues de que se obtiene el resultado de una ronda y la mano es agregada en la variable hands
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
                tempCardWin = tempResultHand['player'].getCardTheNumberHand(numberTheCurrentHand).getValue()
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

    def getResultHandByNumber(self, numberHand):
        ''' Devuelve el resultado de una mano por su numero de mano '''
        return self.hands[numberHand]

    def getStatusTheRound(self):
        '''
            Esta funcion devuelve el resultado de la mano jugada y devuelve el estado que termino la mano
            @params
            null

            @return
            {
                'player': object Player,
                'parda': bool
            }
        '''

        resultCurrentHand = self.getResultCurrentHand()
        numberTheCurrentHand = self.getNumberTheCurrentHand()
        self.addResultHand(resultCurrentHand)
        if numberTheCurrentHand == 0:
            ''' En la primera mano se duelve el resultado sin ninguna comprobacion '''
            return resultCurrentHand
        elif numberTheCurrentHand > 0:
            numberThePreviusHand = numberTheCurrentHand-1
            winner = False
            if resultCurrentHand['parda'] and self.getResultHandByNumber(numberThePreviusHand)['parda']:
                msg_info(' En la mano actual y en la anterior ocurrio una parta: \n \
                El Juego continua siempre y cuando esto ocurra en la segunda ronda \n \
                En el caso de que esto ocurra en la tercera mano el jugador mano de la primera mano es el ganador de la ronda')
                if numberTheCurrentHand != 1:
                    winner = self.getResultHandByNumber(0)
            elif not resultCurrentHand['parda'] and self.getResultHandByNumber(numberThePreviusHand)['parda']:
                msg_info(' En la mano anterior ocurrio una parda pero en la mano actual no \n \
                El ganador de la mano actual es el ganador de la ronda')
                winner = resultCurrentHand
            elif resultCurrentHand['parda'] and not self.getResultHandByNumber(numberThePreviusHand)['parda']:
                msg_info(' En la mano anterior no hubo parda pero en la mano actual hay una parda \n \
                El jugador que gano la primera mano es el ganador de la ronda ')
                winner = self.getResultHandByNumber(0)
            elif resultCurrentHand['player'].getTeam() == self.getResultHandByNumber(numberThePreviusHand)['player'].getTeam():
                msg_info(' El Jugador que gana la mano actual es de el mismo equipo que gano la mano anterior \n \
                El jugador de la mano actual es el ganador de la ronda')
                winner = self.getResultHandByNumber(numberTheCurrentHand)
            elif resultCurrentHand['player'].getTeam() != self.getResultHandByNumber(numberThePreviusHand)['player'].getTeam():
                msg_info(' C0: El jugador que gana la mano actual no es del mismo equipo que gano la mano anterior \n \
                El Juego continua siempre y cuando ocurra en la segunda mano \n \
                Si esto ocurre en la tercera mano se verifica si el ganador de la mano es igual a el ganador de la primera mano')
                if numberTheCurrentHand == 1:
                    self.statusGame = 3
                elif numberTheCurrentHand == 2:
                    if passresultCurrentHand['player'].getTeam() == self.getResultHandByNumber(0)['player'].getTeam():
                        winner = self.getResultHandByNumber(0)
                    elif resultCurrentHand['player'].getTeam() == self.getResultHandByNumber(1)['player'].getTeam():
                        winner = self.getResultHandByNumber(1)
            if winner != False:
                self.statusGame = 0
                return winner

    def empate(self):
        ''' Esta funcion cofigura la estructura del resultado cuando hay una parda '''
        self.returnbtenerGanador['status'] = 2
        self.returnbtenerGanador['roundWin'] = 1
        self.returnbtenerGanador['teamWin'] = self.hand

    def winnerTheRound(self):
        self.returnbtenerGanador['status'] = 0
        self.returnbtenerGanador['roundWin'] = 1

    def parda(self):
        self.returnbtenerGanador['status'] = 1

    def continueRound(self):
        self.returnbtenerGanador['status'] = 3

    def showPointsTeams(self):
        ''' Muestra los puntos de los equipos '''
        for team in self.teams:
            self.actionGame.showPoints(team.getID(), team.getPoints())
            #print ('points team %d: %d') %(team, self.teamPoints[team])

    def start(self):
        msg_debug("Iniciando Juego")
        self.actionGame.setPlayers(self.players)
        while 1:
            self.showPointsTeams()
            ''' Repartir cartas '''
            self.giveCardsToPlayers()
            self.hands = []
            while 1:
                nrond = self.startHand()
                ''' Se inicia el juego con el jugador que es hand '''
                self.actionGame.showMsgStartHand(nrond)
                cJugadas = 0 #Alamacena la cantidad de jugadas en la rond
                while cJugadas < self.numberPlayers:
                    '''Se inicia el juego'''
                    cJugadas += 1
                    jugador = self.getTurn()

                    while 1:
                        cartaAJugar = self.actionGame.getActionPlayer(jugador.getID())
                        if(1 == 1):
                            if(jugador.playingCardInRound(cartaAJugar)): #Juega la carta y se comprueba que este disponible
                                cartaJ = jugador.getNameCardPlayed() #Obitene el nombre completo de la carta
                                #self.giveCard(jugador.getID(),cartaJ)
                                self.actionGame.showJugada(jugador.getTeam().getID(), jugador.getID(), jugador.getName(),cartaJ)
                                break
                            else:
                                self.actionGame.showError(jugador.getID(), 'cardPlayerd')
                        else:
                            self.actionGame.showError(jugador.getID(), 'invalidAction')



                Resultados = self.getStatusTheRound()
                #ResultHand = self.getResultCurrentHand()
                self.actionGame.returnStatus(Resultados)
                #print Resultados

                if(self.statusGame == 1):
                    self.actionGame.Parda()
                    continue
                '''elif self.statusGame == 3:
                    continue'''

                RPlayer = Resultados['player']
                self.actionGame.showResultaTheHand(RPlayer.getID(), RPlayer.getName(),  RPlayer.getTeamID(),  RPlayer.getNameCardPlayed())
                if(self.statusGame == 0):
                    if(self.statusGame == 0):
                        self.actionGame.win(Resultados['player'].getTeamID())
                    elif(self.statusGame == 2):
                        self.actionGame.winEmpate(Resultados['player'].getTeamID())
                    self.givePointsTeam(Resultados['player'].getTeam(),2)
                    self.resetRond()
                    break

                self.finishRound()
            break
        msg_debug("Juego Terminado")
    def finishRound(self):
        pass
