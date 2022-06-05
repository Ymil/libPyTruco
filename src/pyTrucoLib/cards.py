#!/usr/bin/env python 2.7

__author__ = 'Lautaro Linquiman'
__email__ = 'acc.limayyo@gmail.com'
__status__ = 'Developing'
__date__ = '06-01-2015'

from copy import copy
from random import randrange
from .card import Card


class Cards():
    '''Clase encargada de el manejo de las cartas del juego'''

    def __init__(self):
        '''
        Puntaje de cada carta
        4 = 1
        5 = 2
        6 = 3
        7 Basto y Copa = 4
        10 = 5
        11 = 6
        12 = 7
        As Oro Y Copo = 8
        2 = 9
        3 = 10
        7 Oro = 11
        7 Espada = 12
        1 Basto = 13
        1 Espada = 14
        '''
        self.cartas = [
            # [Numero de carta, palo, valor]
            [1, 'oro', 8],  [1, 'espada', 14],
            [1, 'basto', 13], [1, 'copa', 8],
            [2, 'oro', 9],  [2, 'espada', 9],
            [2, 'basto', 9],  [2, 'copa', 9],
            [3, 'oro', 10], [3, 'espada', 10],
            [3, 'basto', 10], [3, 'copa', 10],
            [4, 'oro', 1],  [4, 'espada', 1],
            [4, 'basto', 1],  [4, 'copa', 1],
            [5, 'oro', 2],  [5, 'espada', 2],
            [5, 'basto', 2],  [5, 'copa', 2],
            [6, 'oro', 3],  [6, 'espada', 3],
            [6, 'basto', 3],  [6, 'copa', 3],
            [7, 'oro', 11], [7, 'espada', 12],
            [7, 'basto', 4],  [7, 'copa', 4],
            [10, 'oro', 5], [10, 'espada', 5],
            [10, 'basto', 5], [10, 'copa', 5],
            [11, 'oro', 6], [11, 'espada', 6],
            [11, 'basto', 6], [11, 'copa', 6],
            [12, 'oro', 7], [12, 'espada', 7],
            [12, 'basto', 7], [12, 'copa', 7],
        ]

        self.clonCartas = []
        self.cartasRepartidas = []

    def __clonarCartas(self):
        self.clonCartas = copy(self.cartas)

    def prepararMaso(self):
        '''Esta funcion copia los valores y nombres de las
         cartas en una variable temporal.
         Esta funcion se debe llamar antes de repartir las cartas '''
        self.__clonarCartas()

    def repartir_individual(self):
        ''' Esta funcion reparte 3 cartas
        Return list (1,2,3)'''

        cartasJugador = []  # Acomoda las cartas de cada jugador

        for _ in range(3):  # reparte tres cartas aleatorias
            cartaN = randrange(0, len(self.cartas) - 1)
            cartaList = self.cartas[cartaN]
            cartaObject = Card(cartaList)
            cartasJugador.append(cartaObject)
            self.cartas.remove(cartaList)
            del cartaObject

        return cartasJugador
