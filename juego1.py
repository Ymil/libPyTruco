import sys
from cartas import Cartas
from accionesJuego import AccionesJuego
import logging
logging.basicConfig(format='%(levelname)s [%(asctime)s][SVR]: %(message)s',filename='./logs/libjuego.log', level='DEBUG')
import inspect
import time
global cuentaEjecucion
cuentaEjecucion = 0
import string
def msg_debug(str1):
        global cuentaEjecucion
        #if(type(str1) is list):
        #    str1 = ' | '.join(tuple(list(str1))[0:])
        #print cuentaEjecucion
        str1 = 'EC %d' % cuentaEjecucion, str1
        #str1 = string.join(, ' ')
        logging.debug(str1)
        cuentaEjecucion += 1
class Game():
        ''' Clase controlador del Juego
        20-01-15 05:07 Lautaro Linquiman'''
        def __init__(self, players, players_team, tableID):
                self.status = 0
                self.players = players
                self.players_team = players_team
                self.numberPlayers = len(players) #Obtiene la cantidad de jugadores
                self.cardPlayer = [] # Cartas de jugador
                self.playsCard = {} #Cartas jugadas
                self.teamPoints = {1:0,2:0}
                self.winningTeamFirstRound = 0 #team ganador de la primera rond
                self.winningTeamSecondRound = 0
                #self.primerJugadorPartida = 0
                self.tableID = tableID
                self.pardaObtenerGanador = 0
                self.rond = 0
                self.ronds = {}
                self.hands = {} # Guarda el resultado de las manos de la ronda
                self.hand = 0
                self.turn = 0
                self.cards = Cartas(self.numberPlayers, 0)
                self.actionGame = AccionesJuego()
                self.returnbtenerGanador = {
                        'status':0,
                        'playerid': 0,
                        'playeridWin': 0,
                        'playerTeam': 0,
                        'teamWin': 0,
                        'roundWin': 0,
                        'card': '', #str Type
                        'cardWin': 0,
                }
                self.returnbtenerGanador = self.returnbtenerGanador


	self.resultLastHand = [] # Resultado de la ultima mano


        def setActionGame(self, classActionGame):
                self.actionGame = classActionGame()

        def getStatus(self):
                return self.status

        def setStatus(self,status):
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

        def startRound(self):
                ''' Se inicia la una nueva ronda y se asigna el turno al jugador indicado '''
                self.rond += 1
                self.ronds[self.rond] = []
                self.hand = self.getTurn()
                return self.rond

        def resetRond(self):
                self.rond = 0
                self.pardaObtenerGanador = 0

        def getRond(self):
                return self.rond

        def giveCardsToPlayers(self):
                ''' Se reparten las cartas de los jugadores '''
                cardPlayers = self.cards.repartir()
                for cardsPlayer in cardPlayers:
			for jugador in self.players:
					self.actionGame.giveCards(jugador.getID(), cardsPlayer);
					jugador.setCards(cardsPlayer)
					self.actionGame.showCards(jugador.getID(), cardsPlayer)

        '''def darCartas(self, playerID):
		self.playsCard[playerID] = []
                return self.cardPlayer[playerID]'''

        def giveCard(self, playerID, cardID):
                '''Asigna la carta jugada en la determinada ronda'''
                nrond = self.getRond()
                self.ronds[nrond].append((playerID, cardID))

        def givePointsTeam(self, teamID, points):
                self.teamPoints[teamID] += points

        def getPointsTeams(self):
                return self.teamPoints
	def getNumberTheCurrentHand(self):
		return len(self.hands)

	def getResultCurrentHand(self):
		'''Devuelve el ganador de la mano
		return
		{'player': object Player, 'parda': bool}
		'''

		numberTheCurrentHand = self.getNumberTheCurrentHand()
		tempResultHand = {'player': False, 'parda': False} #Resultado temporal de la mano
		for player in self.players: #No concuerda con la mano, falta terminar esto.
			try:
				tempCardWin = tempResultRound['player'].getCardTheNumberHand(numberTheCurrentHand)
			except: #Esta exception se captura cuando todavia no hay un jugador en el resultado ganador
				tempCardWin = 0

			playsCard = player.getCardTheNumberHand(numberTheCurrentHand)

			if tempCardWin < playsCard:
                                tempResultRound['player'] = player
                                tempResultRound['parda'] = False
                        else if tempCardWin == playsCard:
                                #Hay una parda
                                tempResultRound['parda'] = True

		return tempResultHand

	def addResultHand(self, resultHand):
		''' Agrega un resultado a la lista de manos '''
		self.hands.append(resultHand)

	def getResultHandByNumber(self, numberHand):
		''' Devuelve el resultado de una mano por su numero de mano '''
		return self.hands[numberHand]

	def getStatusTheRound(self):
		'''
			Esta funcion busca un ganador de la mano jugada y devuelve el estado que termino la mano
			@params
			null

			@return
			{
				'status': int [0:win|1:parda|2:empate|3:continue],
				'playerid': [idJugadorGanador],
				'teamWin': [idteamGanador]
				'cardWin': [CartaGandora],
				'roundWin': int Se gano la rond [0|1]
			}
                '''

		resultCurrentHand = self.getResultHand()
		self.addResultHand(resultTheActualHand)
		numberTheCurrentHand = self.getNumberTheCurrentHand()
		if numberTheCurrentHand == 0:
			return resultCurrentHand
		elif numberTheCurrentHand > 0:
			numberThePreviusHand = resultCurrentHand-1
			if resultCurrentHand['parda'] and self.getResultHandByNumber(numberThePreviusHand)['parda']:
				''' En la mano actual y en la anterior ocurrio una parta:
				El Juego continua siempre y cuando esto ocurra en la segunda ronda
				En el caso de que esto ocurra en la tercera mano el jugador mano de la primera mano es el ganador de la ronda'''
				if numberTheCurrentHand == 1:
					continue_game()
				else:
					return self.getResultHandByNumber(0)
			if not resultCurrentHand['parda'] and self.getResultHandByNumber(numberThePreviusHand)['parda']:
				''' En la mano anterior ocurrio una parda pero en la mano actual no
				El ganador de la mano actual es el ganador de la ronda'''
				return self.resultCurrentHand
			elif resultCurrentHand['parda'] and not self.getResultHandByNumber(numberThePreviusHand)['parda']:
				''' En la mano anterior no hubo parda pero en la mano actual hay una parda
				El jugador que gano la primera mano es el ganador de la ronda '''
				return self.getResultHandByNumber(0)
			elif resultCurrentHand['player'].getTeam() == self.getResultHandByNumber(numberThePreviusHand)['player'].getTeam():
				''' El Jugador que gana la mano actual es de el mismo equipo que gano la mano anterior
				El jugador de la mano actual es el ganador de la ronda'''
				return winner
			elif resultCurrentHand['player'].getTeam() != self.getResultHandByNumber(numberThePreviusHand)['player'].getTeam():
				''' El jugador que gana la mano actual no es del mismo equipo que gano la mano anterior
				El Juego continua siempre y cuando ocurra en la segunda mano
				Si esto ocurre en la tercera mano se verifica si el ganador de la mano es igual a el ganador de la primera mano'''
				if numberTheCurrentHand == 1:
					return continue
				elif numberTheCurrentHand == 2 and resultCurrentHand['player'].getTeam() == self.getResultHandByNumber(0)['player'].getTeam():


        def getWinner(self):
                '''
                Esta funcion busca un ganador de la hand jugada y devuelve el estado que termino la hand
                @params
                null

                @return
                {
                        'status': int [0:win|1:parda|2:empate|3:continue],
                        'playerid': [idJugadorGanador],
                        'teamWin': [idteamGanador]
                        'cardWin': [CartaGandora],
                        'roundWin': int Se gano la rond [0|1]
                }
                '''

                nrond = self.getRond()

                '''
                cartaMayor[0] Indica la carta ganadora
                returnbtenerGanador['playerid'] Indica el IDjugador ganador
                '''

                parda = 0
                msg_debug('Ejecutando %s' % inspect.stack()[0][3])
                str1 = 'ronds ', len(self.ronds),'/', self.ronds
                msg_debug(str1)
                self.returnbtenerGanador['cardWin'] = 0
                for rond in self.ronds[nrond]:
                        #print dir(rond)

                        self.returnbtenerGanador['playerid'] = rond[0]
                        self.returnbtenerGanador['playerTeam'] = self.players_team[self.returnbtenerGanador['playerid']]
                        self.returnbtenerGanador['card'] = rond[1]

                        msg_debug('[getWinner-cartaSTR] %s' % self.returnbtenerGanador['card'])
                        puntajeCartaJugador = self.cards.getPoints(self.returnbtenerGanador['card'])
                        if(nrond == 1):
                                ''' Se setean la variables para start el juego '''
                                self.winningTeamFirstRound = 0
                                self.winningTeamSecondRound = 0
                                self.pardaObtenerGanador = 0

                        if(self.returnbtenerGanador['cardWin'] == 0):
                                msg_debug("[Carta Ganadora] Todavia no hay una carta ganadora")
                                puntajeCartaMayor = 0
                        else:
                                puntajeCartaMayor = self.cards.getPoints(self.returnbtenerGanador['cardWin'])
                                msg_debug("[Carta Ganadora] %s:%d" % (self.returnbtenerGanador['cardWin'], puntajeCartaMayor))
                        if(puntajeCartaJugador > puntajeCartaMayor):
                                self.returnbtenerGanador['playeridWin'] = self.returnbtenerGanador['playerid']
                                self.returnbtenerGanador['teamWin'] = self.returnbtenerGanador['playerTeam']
                                self.returnbtenerGanador['cardWin'] = self.returnbtenerGanador['card']
                                parda = 0
                        elif(puntajeCartaJugador == puntajeCartaMayor):
                                self.returnbtenerGanador['cardWin'] = self.returnbtenerGanador['card']
                                parda = 1
                print(self.returnbtenerGanador['teamWin'])
                teamWinhandActual = self.returnbtenerGanador['teamWin']
                msg_debug("Parda %d" % parda)
                if(self.rond == 1):
                        if(parda == 1):
                                self.pardaObtenerGanador = 1
                                self.parda()
                        print 'oh'
                        self.winningTeamFirstRound = teamWinhandActual
                        self.setTurn(self.returnbtenerGanador['playeridWin'])
                        self.continueRound()
                elif(self.rond == 2):
                        if(self.pardaObtenerGanador == 1 or parda == 1):
                                if(parda == 0):
                                        self.winnerTheRound()
                                elif((parda == 0 and self.pardaObtenerGanador == 1) or (parda == 1 and self.pardaObtenerGanador == 0)):
                                        self.returnbtenerGanador['teamWin'] = self.winningTeamSecondRound
                                        self.winnerTheRound()
                                elif(parda == 1 and self.pardaObtenerGanador == 1):
                                        self.parda()

                        self.winningTeamSecondRound = teamWinhandActual
                        if(teamWinhandActual == self.winningTeamFirstRound):
                                self.winnerTheRound()
                        else:
                                self.continueRound()
                                self.setTurn(self.returnbtenerGanador['playerid'])

                elif(self.rond == 3):
                        if(self.pardaObtenerGanador == 1 or parda == 1):
                                if(parda == 0):
                                        self.winnerTheRound()
                                elif(parda == 1):
                                        self.empate()
                        msg_debug("team Ganador hand Actual: %s" % teamWinhandActual)
                        msg_debug("team Ganador hand 2: %s" % self.winningTeamSecondRound)
                        msg_debug("team Ganador hand 1: %s" % self.winningTeamFirstRound)
                        if(teamWinhandActual == self.winningTeamFirstRound):
                                self.winnerTheRound()
                        elif(teamWinhandActual == self.winningTeamSecondRound):
                                self.returnbtenerGanador['teamWin'] = self.winningTeamSecondRound
                                self.winnerTheRound()
                        msg_debug(self.returnbtenerGanador)
                return self.returnbtenerGanador

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
		for team in self.getPointsTeams():
			self.actionGame.showPoints(team, self.teamPoints[team])
			#print ('points team %d: %d') %(team, self.teamPoints[team])
        def start(self):
                msg_debug("Iniciando Juego")
                self.actionGame.setTeams(self.players_team)
                self.actionGame.setPlayers(self.players)
                while 1:
			self.showPointsTeams()
                        ''' Repartir cartas '''
                        self.giveCardsToPlayers()

                        while 1:
                                nrond = self.startRound()
                                ''' Se inicia el juego con el jugador que es hand '''
                                cJugadas = 0 #Alamacena la cantidad de jugadas en la rond
                                while cJugadas < self.numberPlayers:
                                        '''Se inicia el juego'''
                                        cJugadas += 1
                                        jugador = self.getTurn()

                                        while 1:
                                                cartaAJugar = self.actionGame.getActionPlayer(jugador.getID())
                                                carta = self.decCartaID(cartaAJugar) #Corrobora que el valor de la carta sea correcto
                                                if(not carta == 20):
                                                        if(jugador.playingCard(carta)): #Juega la carta y se comprueba que este disponible
                                                                cartaJ = jugador.getCardPlayed() #Obitene el nombre completo de la carta
                                                                self.giveCard(jugador.getID(),cartaJ)
                                                                self.actionGame.showJugada(jugador.getTeam(), jugador.getID(), jugador.getName(),cartaJ)
                                                                break
                                                        else:
                                                                self.actionGame.showError(jugador.getID(), 'cardPlayerd')
                                                else:
                                                        self.actionGame.showError(jugador.getID(), 'invalidAction')
                                Resultados = self.getWinner()
                                self.actionGame.returnStatus(Resultados)
                                print Resultados

                                if(Resultados['status'] == 1):
                                        self.actionGame.Parda()
                                        continue

                                self.actionGame.showResulthand(Resultados['playeridWin'], self.players[Resultados['playeridWin']].getName(),  Resultados['playerTeam'],  Resultados['cardWin'])
                                if(Resultados['roundWin']):
                                        if(Resultados['status'] == 0):
                                                self.actionGame.win(Resultados['teamWin'])
                                        elif(Resultados['status'] == 2):
                                                self.actionGame.winEmpate(Resultados['teamWin'])
                                        self.givePointsTeam(Resultados['teamWin'],2)
                                        self.resetRond()
                                        break

                        break
                msg_debug("Juego Terminado")
