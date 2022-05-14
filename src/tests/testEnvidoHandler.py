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
from handlers.signals import signals
import pdb

print("Iniciando test".center(len(__descripcion__), "-"))
print(__descripcion__)
print("".center(len(__descripcion__), "-"))

@mock.patch("juego.Game.giveCardsToPlayers", return_value=None)
class testTrucoHandler(TestCase):
    def setUp(self):
        """ Paso 1: Definiendo parametros de la simulacion """
        self.cantidadDeJugadores = 2

        """Paso 2: Definiendo jugadores"""
        self.jugadores = []
        self.jugadores.append(Jugador(1))
        self.jugadores.append(Jugador(2))

        self.jugadores[0].setCards(
            [Card([1, "espada", 14]), Card([7, "oro", 11]), Card([7, "espada", 12])]
        )
        self.jugadores[1].setCards(
            [Card([1, "oro", 8]), Card([1, "basto", 13]), Card([3, "basto", 10])]
        )

        """ Paso : Creando mesa """
        self.mesa = Mesa(self.cantidadDeJugadores, self.jugadores[0].getID(), 0)

        """Paso 4: Asignando nuevos jugadores a la mesa"""
        self.mesa.newPlayer(self.jugadores[0])
        self.mesa.newPlayer(self.jugadores[1])

        self.game = Game(self.mesa, signals())
    
    @mock.patch("envido_handler.get_response")
    def test_verify_envido_quiero(self, mock_response, *args):
        self.game.startRound()
        mock_response.return_value = ("quiero", 1)

        # Inicio de la pimera mano
        self.game.startHand()
        self.game._envidoHandler.envido_handler(self.jugadores[0])

        self.assertEqual(self.jugadores[0].team.getPoints(), 2)

    @mock.patch("envido_handler.get_response")
    def test_verify_envido_no_quiero(self, mock_response, *args):
        mock_response.return_value = ("quiero", 0)

        
        self.game.startRound()

        # Inicio de la pimera mano
        self.game.startHand()
        self.game._envidoHandler.envido_handler(self.jugadores[0])

        self.assertEqual(self.jugadores[0].team.getPoints(), 1)   

    @mock.patch("envido_handler.get_response", side_effect=[
        ("envido", 0), ("real_envido", 0), ("real_envido", 0),
        ("quiero", 1) 
    ])
    def test_verify_envido_acumulation_quiero(self, *args):

        self.game.startRound()

        # Inicio de la pimera mano
        self.game.startHand()
        self.game._envidoHandler.envido_handler(self.jugadores[0])

        self.assertEqual(self.jugadores[0].team.getPoints(), 10) 


if "__main__" == __name__:
    unittest.main()
