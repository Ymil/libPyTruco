#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-

__author__ = "Lautaro Linquiman"
__email__ = "acc.limayyo@gmail.com"
__status__ = "Developing"

from accionesJuego import AccionesJuego

import sys

sys.path.append("../src")

'''
Simulacion de ejemplo de como utilizar la libreria PyTruco

Paso 1: Definir parametros de la Simulacion
    CantidadDeJugadores

Paso 2: Definir jugadores
Se importa el modulo jugador, el cual alamacena todos los parametros y funcionalidades.
'''
from jugador import Jugador

'''
Paso 3: Crear mesa
Se importa el modulo mesa, el cual alamacena todos los parametros y funcionalidades.
'''
from mesa import Mesa

''' Paso 5: Crear una nueva partida
Se importa el modulo Juego, el cual alamacena todos los parametros y funcionalidades.
'''
from juego import Game


class EjemploDeTruco:
    def __init__(self):
        ''' Paso 1: Definiendo parametros de la simulacion '''
        self.cantidadDeJugadores = 2

        '''Paso 2: Definiendo jugadores'''
        self.jugadores = []
        self.jugadores.append(Jugador(1))
        self.jugadores.append(Jugador(2))

        ''' Paso : Creando mesa '''
        self.mesa = Mesa(self.cantidadDeJugadores, self.jugadores[0].getID(), 0)

        '''Paso 4: Asignando nuevos jugadores a la mesa'''
        self.mesa.newPlayer(self.jugadores[0])
        self.mesa.newPlayer(self.jugadores[1])

        #Se verifica que se pueda iniciar la partida
        if(self.mesa.getStatus()):
            ''' Paso 6: Se crea una nueva instancia de juego, con todos los parametros para poder crear la mesa '''
            self.juego = Game(self.mesa, AccionesJuego())
            ''' Paso 7: se inicia la partida y se comienza el juego en modo automatico con bots '''
            self.juego.start()
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
    EjemploDeTruco()
