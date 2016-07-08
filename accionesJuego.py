import logging
#logging.basicConfig(format='[AccionesJuego] %(levelname)s [%(asctime)s]: %(message)s',filename='./logs/libjuego.log', level='DEBUG')
import random

class AccionesJuego:
    '''
    Esta clase almacena los eventos que se disparan a medida que se va ejecuntado el juego.

    Como mostrar mensajes, dar cartas etc.

    Esta clase es de ejemplo
    '''
    def __init__(self):
        self.players = []
        self.teams = []
        self.errors = {'cardPlayerd': 'Esta carta ya fue jugada', 'invalidAction': 'No puedes realizar esta accion'}
    def startGame(self, players):
        print ""
    def setPlayers(self, players):
        self.players = players

    def setTeams(self, teams):
        self.teams = teams

    def giveCards(self, playerid, cards):
        ''' Esta funcion se dispara cuando se reparten las cartas,
        recibe como parametro el playerid y las cartas del jugador

        Ejemplo de uso:
        partida.mostrarCartas(player, cards) '''

        pass
    def showCards(self, playerid, cards):
        ''' Esta funcion se dispara cuando se le muestran las cartas al jugador
        params
        @playerid: int
        @cartas: [3]
        Ejemplo de uso:
        '''
        print 'Cartas de Jugador',playerid,':', cards

    def showPoints(self, team, pointsTeam):
        ''' Esta funcion se dispara cuando se muestran los puntos de los equipos
        @team: int teamID
        @pointsTeam: int
        Ejemplo de uso: '''

        print "El equipo %d tiene %d puntos" % (team, pointsTeam)

    def getActionPlayer(self, playerid):
        ''' Esta funcion se llama cuando se tiene que obtener un accion del jugador
        @params
        @playerid: int
        Ejemplo:
        accion = raw_input("Escriba la accion o carta a jugar>")
        return accion
        '''

        return random.randint(1,3)

    def showJugada(self, teamid, playerid, playername, cardGaming):
        ''' Esta funcion se llama cuando se juega una carta
        @params
        @playerid: int
        @playername: str Nombre del jugador
        @cardGaming: int Carta jugada
        Ejemplo:
        '''
        print 'El jugador %d:%d jugo la carta %s' % (teamid, playerid, cardGaming)

    def showError(self, playerid, errorName):
        ''' Esta funcion se llama cuando ocurre un error por un jugador
        @params
        @playerid: int
        @errorName: str ['cardPlayerd', 'invalidAction']
        Ejemplo:
        '''
        #print self.errors[errorName]
        pass

    def showResultMano(self, playerid, playername, teamid, card):
        ''' Esta funcion se llama cuando termina una mano
        @params
        @playerid: int
        @playername: str Nombre del jugador
        @teamID: int
        @card: int Carta
        Ejemplo:'''
        print '%d:%d gano la mano con %s' % (teamid, playerid, card)

    def Parda(self):
        ''' Esta funcion se llama cuando termina la mano y hay una parda
        @params
        none'''
        print 'Ocurrio una parda'

    def returnStatus(self, statusGame):
        ''' Esta funcion se llama cada vez que se busca un ganador
        @params
        @statusGame: [StatusGame=(win,empate), teamWinner], [StatusGame=empate, CartaMayor], [StatusGame=continue, CartaMayor, playerid]
        '''
        #logging.debug("ReturnStatus")
        #print 'Status:',statusGame
        pass

    ''' Win Actions '''
    def winEmpate(self, teamIDWinner):
        ''' Esta funcion se llama cuando ocurre un empate
        @params
        @teamIDWinner: int
        '''
        print 'Ocurrio un empate, los puntos son para el equipo %d' % teamIDWinner

    def win(self, teamIDWinner):
        ''' Esta funcion se llama cuando se gana la ronda
        @params
        @teamIDWinner: int
        '''
        print 'El equipo %s gano la ronda' % teamIDWinner
