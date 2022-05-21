#!/usr/bin/env python 2.7
from pyTrucoLib.juego import Game
from pyTrucoLib.jugador import Jugador
from pyTrucoLib.table import Table
__author__ = 'Lautaro Linquiman'
__email__ = 'acc.limayyo@gmail.com'
__status__ = 'Developing'

from accionesJuego import AccionesJuego


class EjemploDeTruco:
    def __init__(self):
        ''' Paso 1: Definiendo parametros de la simulacion '''
        self.cantidadDeJugadores = 2

        '''Paso 2: Definiendo jugadores'''
        self.jugadores = []
        self.jugadores.append(Jugador(1))
        self.jugadores.append(Jugador(2))

        ''' Paso : Creando mesa '''
        self.mesa = Table(
            self.cantidadDeJugadores,
            self.jugadores[0].getID(), 0,
        )

        '''Paso 4: Asignando nuevos jugadores a la mesa'''
        self.mesa.newPlayer(self.jugadores[0])
        self.mesa.newPlayer(self.jugadores[1])

        # Se verifica que se pueda iniciar la partida
        if(self.mesa.getStatus()):
            ''' Paso 6: Se crea una nueva instancia de juego,
            con todos los parametros para poder crear la mesa '''
            self.juego = Game(self.mesa, AccionesJuego())
            ''' Paso 7: se inicia la partida y se comienza el
             juego en modo automatico con bots '''
            self.juego.start()


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()
    EjemploDeTruco()
