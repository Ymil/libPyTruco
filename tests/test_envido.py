#!/usr/bin/env python 2.7
from unittest import mock
from unittest import TestCase

from pyTrucoLib.card import Card
from pyTrucoLib.handlers.signals import signals
from pyTrucoLib.juego import Game
from pyTrucoLib.jugador import Jugador
from pyTrucoLib.mesa import Mesa


@mock.patch('pyTrucoLib.juego.Game.giveCardsToPlayers', return_value=None)
class testTrucoHandler(TestCase):
    def setUp(self):
        """ Paso 1: Definiendo parametros de la simulacion """
        self.cantidadDeJugadores = 2

        """Paso 2: Definiendo jugadores"""
        self.jugadores = []
        self.jugadores.append(Jugador(1))
        self.jugadores.append(Jugador(2))

        self.jugadores[0].setCards(
            [
                Card([1, 'espada', 14]), Card(
                    [7, 'oro', 11],
                ), Card([7, 'espada', 12]),
            ],
        )
        self.jugadores[1].setCards(
            [
                Card([1, 'oro', 8]), Card([1, 'basto', 13]),
                Card([3, 'basto', 10]),
            ],
        )

        """ Paso : Creando mesa """
        self.mesa = Mesa(
            signals(),
            self.cantidadDeJugadores,
            self.jugadores[0].getID(), 0,
        )

        """Paso 4: Asignando nuevos jugadores a la mesa"""
        self.mesa.newPlayer(self.jugadores[0])
        self.mesa.newPlayer(self.jugadores[1])

        self.game = Game(self.mesa)

    @mock.patch('pyTrucoLib.envido_handler.get_response')
    def test_verify_envido_quiero(self, mock_response, *args):
        self.game.startRound()
        mock_response.return_value = ('quiero', 1)

        # Inicio de la pimera mano
        self.game.startHand()
        self.game._envidoHandler.envido_handler(self.jugadores[0])

        self.assertEqual(self.jugadores[0].team.getPoints(), 2)

    @mock.patch('pyTrucoLib.envido_handler.get_response')
    def test_verify_envido_no_quiero(self, mock_response, *args):
        mock_response.return_value = ('quiero', 0)

        self.game.startRound()

        # Inicio de la pimera mano
        self.game.startHand()
        self.game._envidoHandler.envido_handler(self.jugadores[0])

        self.assertEqual(self.jugadores[0].team.getPoints(), 1)

    @mock.patch(
        'pyTrucoLib.envido_handler.get_response', side_effect=[
            ('envido', 0), ('real_envido', 0), ('real_envido', 0),
            ('quiero', 1),
        ],
    )
    def test_verify_envido_acumulation_quiero(self, *args):

        self.game.startRound()

        # Inicio de la pimera mano
        self.game.startHand()
        self.game._envidoHandler.envido_handler(self.jugadores[0])

        self.assertEqual(self.jugadores[0].team.getPoints(), 10)
