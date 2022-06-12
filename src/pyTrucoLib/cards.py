#!/usr/bin/env python 2.7

__author__ = 'Lautaro Linquiman'
__email__ = 'acc.limayyo@gmail.com'
__status__ = 'Developing'
__date__ = '06-01-2015'

from copy import copy
from random import randrange
from .card import Card, cards_dict


class Cards():
    '''Clase encargada de el manejo de las cartas del juego'''

    def __init__(self):
        self.clonCartas = []
        self.cartasRepartidas = []

    def __clonarCartas(self):
        self.clonCartas = copy(cards_dict)

    def prepararMaso(self):
        '''Esta funcion copia los valores y nombres de las
         cartas en una variable temporal.
         Esta funcion se debe llamar antes de repartir las cartas '''
        self.__clonarCartas()

    def repartir_individual(self):
        ''' Esta funcion reparte 3 cartas
        Return list (1,2,3)'''

        cartasJugador = []  # Acomoda las cartas de cada jugador
        cards_keys = self.clonCartas.keys()
        for _ in range(3):  # reparte tres cartas aleatorias
            cartaN = randrange(0, len(cards_keys) - 1)
            card_name = self.cartas[cartaN]
            cartaObject = Card(card_name)
            cartasJugador.append(cartaObject)
            del self.clonCartas[card_name]
            del cartaObject

        return cartasJugador
