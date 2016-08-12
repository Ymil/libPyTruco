'''
clase Jugador Servidor
09-01 06:24
Lautaro Linquiman
'''
import pdb;
class Jugador():
    def __init__(self, id):
        self.idJugador = id #IdCon
        self.status = 0
        self.nombre = ''
        self.team = False
        self.cartas = [] #Almacena las cartas del jugador
        self.cartasJugadas = [] #Almacena las cartas que el jugador ya jugo
        self.ultimaCartaJugada = 0 #Almacena el id de la ultima carta jugada

    def setTeam(self, teamObject):
        self.team = teamObject

    def getTeam(self):
        return self.team
    def getTeamID(self):
        return self.team.getID()

    def setName(self, nombre):
        self.nombre = nombre

    def getName(self):
        ''' Devuelve el nombre del jugador '''
        return self.nombre

    def getID(self):
        '''devuelve el id (IDCON) del jugador '''
        return self.idJugador

    def setCards(self, cartas):
        ''' Se ingresan la cartas que les da el juego '''
        self.resetCards()
        self.cartas = cartas

    def resetCards(self):
        self.cartas = []
        self.cartasJugadas = []
        self.ultimaCartaJugada = 0

    def playingCardInRound(self, cartaID):
        ''' Corrobora que las cartas del jugador sea valida y la juega '''
        carta = self.cartas[cartaID]
        if carta in self.cartasJugadas:
            return 0
        else:
            self.cartasJugadas.append(carta)
            self.ultimaCartaJugada = cartaID
            return 1
    def getCardsPlayer(self):
        ''' Esta funcion devuelve todas las cartas del jugador en forma de areglo '''
        print self.cartas
        return self.cartas

    def getCardTheNumberHand(self, roundNumber):
        ''' Devuelve la carta jugada en la mano x '''
        return self.cartasJugadas[roundNumber]

    def getNameCardPlayed(self):
        ''' Devuelve el nombre completa de la ultima carta jugada '''
        return self.cartas[self.ultimaCartaJugada]

    def setStatus(self, valor):
        self.status = valor

    def getStatus(self):
        return self.status
