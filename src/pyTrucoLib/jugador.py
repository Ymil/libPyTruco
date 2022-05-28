#!/usr/bin/env python 2.7
__author__ = 'Lautaro Linquiman'
__email__ = 'acc.limayyo@gmail.com'
__status__ = 'Developing'
import operator
from collections import Counter


class Jugador():
    def __init__(self, id):
        '''
        Esta clase controla toda la funcionalidad de los jugadores
        09-01-15 06:24
        @author: Lautaro Linquiman
        :param id: int
        :rtype: playerOjbect
        '''
        self.idJugador = id  # IdCon
        self.status = 0
        self.nombre = ''
        self.team = False
        self.cartas = []  # Almacena las cartas del jugador
        self.cartasJugadas = []  # Almacena las cartas que el jugador ya jugo
        self.ultimaCartaJugada = 0  # Almacena el id de la ultima carta jugada

    def setTeam(self, teamObject):
        '''
        :param teamObject:
        '''
        self.team = teamObject

    def getTeam(self):
        ''' :return: equipo del jugador
        :rtype: teamObject '''
        return self.team

    def getTeamID(self):
        ''' :return: ID del equipo del jugador
        :rtype: int '''
        return self.team.getID()

    def setName(self, nombre):
        ''' Asgina el nombre del jugador
        :param nombre: str '''
        self.nombre = nombre

    def getName(self):
        ''' Devuelve el nombre del jugador
        :rtype: str'''
        return self.nombre

    def getID(self):
        '''
        :return: ID del jugador
        :rtype: int'''
        return self.idJugador

    def setCards(self, cartas):
        ''' Se ingresan la cartas que les da el juego
        :param cartas: list cardObjects'''
        self.resetCards()
        self.cartas = cartas

    def resetCards(self):
        ''' Se borran todas las cartas y variables cargadas que tenia el jugador
        '''
        self.cartas = []
        self.cartasJugadas = []
        self.ultimaCartaJugada = 0

    def playing_card(self, cartaID):
        ''' Corrobora que las cartas del jugador sea valida y la juega
        :param cartaID: int
        :rtype: bool
        '''
        carta = self.cartas[cartaID]
        if carta in self.cartasJugadas:
            return False
        else:
            self.cartasJugadas.append(carta)
            self.ultimaCartaJugada = cartaID
            return True

    def getCardsPlayer(self):
        ''' Esta funcion devuelve todas las cartas del jugador en forma de areglo
        :return: lista de cardObject
        :rtype: list
        '''
        # print(self.cartas)
        return self.cartas

    def getCardTheNumberHand(self, roundNumber):
        ''' Devuelve la carta jugada en la mano x
        :param roundNumber: int
        :rtype: cardObject
        '''
        return self.cartasJugadas[roundNumber]

    def getNameCardPlayed(self):
        ''' Devuelve el nombre completa de la ultima carta jugada
        :return: Nombre completo de la carta
        :rtype: str'''
        return self.cartas[self.ultimaCartaJugada]

    def getMaxCard(self):
        '''
        group: player, envido
        Esta funcion devuelve la carta mayor del jugador (Para el envido)
        :return: points
        :rtype: int
        '''
        dicCards = {}
        for carta in self.cartas:
            nCard = carta.getNumber()  # nCard
            if nCard < 10:
                dicCards[nCard] = carta
        if len(dicCards) == 0:
            ''' Todas las cartas del jugador son las consideradas viejas por lo tanto
            tienen valor 0 '''
            return 0
        maxCard = max(dicCards.items(), key=operator.itemgetter(0))
        # pdb.set_trace()
        return maxCard[1].getNumber()

    def getCardByStick(self, stick):
        '''
        group: player, envido
        Agrupa las cartas de un palo determinado
        :param stick: str
        :return: lista de cartas
        :rtype: list'''
        cards = []
        for card in self.cartas:
            if card.getStick() == stick:
                cards.append(card)  # nCard
        return cards

    def getPointsEnvido(self):
        '''
        group: player, envido
        Esta funcion devuelve los puntos que tiene el jugador para el envido
        :return: points
        :rtype: int'''
        cardsSticks = []
        points = 0
        for carta in self.cartas:
            cardsSticks.append(carta.getStick())
        stickEnvido = Counter(cardsSticks).most_common(1)
        if stickEnvido[0][1] == 1:
            points = self.getMaxCard()
        else:
            stick = stickEnvido[0][0]
            card = self.getCardByStick(stick)
            points = card[0]+card[1]
        return points

    def __str__(self):
        return f'Player: {self.getID()} Team: {self.getTeamID()}'
