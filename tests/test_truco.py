from unittest import mock
from unittest import TestCase

from pyTrucoLib.handlers.signals import signals
from pyTrucoLib.juego import Game
from pyTrucoLib.jugador import Jugador
from pyTrucoLib.mesa import Mesa
from pyTrucoLib.truco_handler import TrucoNoQuerido


class testTrucoHandler(TestCase):
    def setUp(self):
        """ Paso 1: Definiendo parametros de la simulacion """
        self.cantidadDeJugadores = 2

        """Paso 2: Definiendo jugadores"""
        self.jugadores = []
        self.jugadores.append(Jugador(1))
        self.jugadores.append(Jugador(2))

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

    def tearDown(self):
        del self.game

    @mock.patch('pyTrucoLib.truco_handler.get_response')
    def test_verify_all_quiero(self, mock_response):
        self.game.startRound()

        # Inicio de la pimera mano
        self.game.startHand()
        mock_response.return_value = ('quiero', 1)
        self.game._truco_handler.truco_handler(self.jugadores[0])
        self.assertEqual(self.game._truco_handler.get_points(), 2)

        self.game._truco_handler.retruco_handler(self.jugadores[1])
        self.assertEqual(self.game._truco_handler.get_points(), 3)

        self.game._truco_handler.vale4_handler(self.jugadores[0])
        self.assertEqual(self.game._truco_handler.get_points(), 4)

    @mock.patch('pyTrucoLib.truco_handler.get_response')
    def test_verify_all_no_quiero(self, mock_response):
        self.game.startRound()

        # Inicio de la pimera mano
        self.game.startHand()
        mock_response.return_value = ('quiero', 0)
        self.assertRaises(
            TrucoNoQuerido,
            self.game._truco_handler.truco_handler, self.jugadores[0],
        )
        self.assertEqual(self.game._truco_handler.get_points(), 1)
        self.assertRaises(
            KeyError, self.game._truco_handler.retruco_handler,
            self.jugadores[1],
        )
        self.assertRaises(
            KeyError, self.game._truco_handler.vale4_handler,
            self.jugadores[0],
        )
