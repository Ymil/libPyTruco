import logging
logging.basicConfig(format='[AccionesJuego] %(levelname)s [%(asctime)s]: %(message)s',filename='./logs/accionGame.log', level='DEBUG')
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

    def showMsgStartGame(self, players):
        ''' Esta funcion se dispara cuando se inicia un nuevo juego
        params
        null
        '''
        logging.debug("startGame")

    def showMsgStartRound(self):
        ''' Esta funcion se dispara cuando se inicia una nueva ronda
        params
        null
        '''
        logging.debug("startRound")

    def showMsgStartHand(self, handsNumber):
        ''' Esta funcion se llama cada vez que se inicia una nueva mano
        params
        handsNumber int'''
        str1 =  ("Iniciando mano %d" % handsNumber).center(50,'-')
        print str1
        logging.debug("startHand(%d)" % handsNumber)
        logging.info(str1)

    def showMsgFinishHand(self):
        ''' Esta funcion se dispara cuando finaliza una mano
        params
        null
        '''
        logging.debug("finishHand")

    def showMsgFinishRound(self):
        ''' Esta funcion se dispara cuando finaliza una ronda
        params
        null
        '''
        logging.debug("finishRound")

    def showMsgFinishGame(self):
        ''' Esta funcion se dispara cuando finaliza un juego
        params
        null
        '''
        logging.debug("finishGame")

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
        cards = [card.getText() for card in cards]
        str1 = 'Cartas de Jugador',playerid,':',cards
        print str1
        str2 = 'showCards(',playerid,',',cards,')'
        logging.info(str1)
        logging.debug(str2)

    def showPoints(self, team, pointsTeam):
        ''' Esta funcion se dispara cuando se muestran los puntos de los equipos
        @team: int teamID
        @pointsTeam: int
        Ejemplo de uso: '''

        str1 = "El equipo %d tiene %d puntos" % (team, pointsTeam)
        print str1
        str2 = "teamPoints(%d,%d)" % (team, pointsTeam)
        logging.debug(str2)
        logging.info(str1)

    def getActionPlayer(self, playerid):
        ''' Esta funcion se llama cuando se tiene que obtener un accion del jugador
        @params
        @playerid: int
        Ejemplo:
        accion = raw_input("Escriba la accion o carta a jugar>")
        return accion
        '''

        return random.randint(0,2)

    def showCardPlaying(self, teamObject, playerObject, card):
        ''' Esta funcion se llama cuando se juega una carta
        @params
        @teamObject
        @playerObject
        @playername: str Nombre del jugador
        @cardGaming: int Carta jugada
        Ejemplo:
        '''
        str1 = 'El jugador %d:%d jugo la carta %s' % (teamObject.getID(), playerObject.getID(), card.getText())
        print str1
        logging.info(str1)
        str2 = 'showCardPlaying(%d,%d,%s)' % (teamObject.getID(), playerObject.getID(), card.getText())
        logging.debug(str2)

    def showError(self, playerid, errorName):
        ''' Esta funcion se llama cuando ocurre un error por un jugador
        @params
        @playerid: int
        @errorName: str ['cardPlayerd', 'invalidAction']
        Ejemplo:
        '''
        #print self.errors[errorName]
        pass

    def showResultaTheHand(self, playerid, playername, teamid, card):
        ''' Esta funcion se llama cuando termina una mano
        @params
        @playerid: int
        @playername: str Nombre del jugador
        @teamID: int
        @card: int Carta
        Ejemplo:'''
        str1 =  '%d:%d gano la mano con %s' % (teamid, playerid, card.getText())
        print str1
        logging.info(str1)
        str2 = 'showResultaTheHand(%d,%d,%s)' % (teamid, playerid, card.getText())
        logging.debug(str2)


    def Parda(self):
        ''' Esta funcion se llama cuando termina la mano y hay una parda
        @params
        none'''
        str1 = 'Ocurrio una parda'
        logging.info(str1)
        logging.debug("parda")

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
        str1 = 'Ocurrio un empate, los puntos son para el equipo %d' % teamIDWinner
        logging.info(str1)

    def win(self, teamIDWinner):
        ''' Esta funcion se llama cuando se gana la ronda
        @params
        @teamIDWinner: int
        '''
        str1 = 'El equipo %s gano la ronda' % teamIDWinner
        logging.info(str1)

    def winGameTeam(self, teamObject):
        ''' Esta funcion se llama cuando un equipo gana el juego
        @params
        @teamObject: object team
        '''
        str1 = 'El equipo %d gano el juego' % teamObject.getID()
        logging.info(str1)
