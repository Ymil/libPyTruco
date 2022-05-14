#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-
__author__ = "Lautaro Linquiman"
__email__ = "acc.limayyo@gmail.com"
__status__ = "Developing"
__date__ = " 04/08/16"
__descripcion__ = "Este teste verifica el correcto funcionamiento del sistema de comparacion de cartas."
from unittest import TestCase, mock
import sys

# Add the ptdraft folder path to the sys.path list
sys.path.append("..")
from card import Card
from mesa import Mesa
from team import Team
from jugador import Jugador
from juego import Game
import utils
from handlers.signals import signals
import pdb

print("Iniciando test".center(len(__descripcion__), "-"))
print(__descripcion__)
print("".center(len(__descripcion__), "-"))


class testTrucoHandler(TestCase):
    def setUp(self):
        """ Paso 1: Definiendo parametros de la simulacion """
        self.cantidadDeJugadores = 2

        """Paso 2: Definiendo jugadores"""
        self.jugadores = []
        self.jugadores.append(Jugador(1))
        self.jugadores.append(Jugador(2))

        """ Paso : Creando mesa """
        self.mesa = Mesa(self.cantidadDeJugadores, self.jugadores[0].getID(), 0)

        """Paso 4: Asignando nuevos jugadores a la mesa"""
        self.mesa.newPlayer(self.jugadores[0])
        self.mesa.newPlayer(self.jugadores[1])

        self.game = Game(self.mesa, signals())

    def tearDown(self):
        del self.game
        
    
    @mock.patch("truco_handler.get_response")
    def test_verify_all_quiero(self, mock_response):
        self.game.startRound()

        # Inicio de la pimera mano
        self.game.startHand()
        mock_response.return_value = ("quiero", 1)
        self.game._truco_handler.truco_handler(self.jugadores[0])
        self.assertEqual(self.game._truco_handler.get_points(), 2)

        self.game._truco_handler.retruco_handler(self.jugadores[1])
        self.assertEqual(self.game._truco_handler.get_points(), 3)

        self.game._truco_handler.vale4_handler(self.jugadores[0])
        self.assertEqual(self.game._truco_handler.get_points(), 4)
    
    @mock.patch("truco_handler.get_response")
    def test_verify_all_no_quiero(self, mock_response):
        self.game.startRound()

        # Inicio de la pimera mano
        self.game.startHand()
        mock_response.return_value = ("quiero", 0)
        self.game._truco_handler.truco_handler(self.jugadores[0])
        self.assertEqual(self.game._truco_handler.get_points(), 1)
        self.assertRaises(KeyError, self.game._truco_handler.retruco_handler, self.jugadores[1])
        self.assertRaises(KeyError, self.game._truco_handler.vale4_handler, self.jugadores[0])


if "__main__" == __name__:
    unittest.main()
