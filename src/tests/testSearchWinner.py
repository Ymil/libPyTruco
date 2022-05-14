import sys  # noqa
import unittest

from card import Card
from handlers.signals import signals
from juego import Game
from jugador import Jugador
from mesa import Mesa

# Add the ptdraft folder path to the sys.path list
sys.path.append('..')  # noqa


class testSearchWinner(unittest.TestCase):
    def test(self):

        game = Game(self.mesa, signals())
        j1: Jugador = self.jugadores[0]
        j2: Jugador = self.jugadores[1]
        # game.setActionGame(signals)
        game.startRound()

        j1.setCards(
            [
                Card([1, 'espada', 14]), Card(
                    [7, 'oro', 11],
                ), Card([7, 'espada', 12]),
            ],
        )
        j2.setCards(
            [
                Card([1, 'oro', 8]), Card([1, 'basto', 13]),
                Card([3, 'basto', 10]),
            ],
        )

        # Inicio de la pimera mano
        game.startHand()

        j1.playingCardInRound(0)
        j2.playingCardInRound(2)

        game.finishHand()
        Resultado = game.resultLastHand
        self.assertEqual(Resultado['player'], j1)
        #
        # Inicio de la segunda mano
        game.startHand()

        j1.playingCardInRound(1)
        j2.playingCardInRound(1)

        game.finishHand()
        Resultado = game.resultLastHand
        self.assertEqual(Resultado['player'], j2)
        # Inicio de la tercera mano
        game.startHand()

        j1.playingCardInRound(2)
        j2.playingCardInRound(0)

        game.finishHand()

        Resultado = game.resultLastHand

        self.assertEqual(Resultado['player'], j1)
        game.finishRound()

    def setUp(self):
        """ Paso 1: Definiendo parametros de la simulacion """
        self.cantidadDeJugadores = 2

        """Paso 2: Definiendo jugadores"""
        self.jugadores = []
        self.jugadores.append(Jugador(1))
        self.jugadores.append(Jugador(2))

        """ Paso : Creando mesa """
        self.mesa = Mesa(
            self.cantidadDeJugadores,
            self.jugadores[0].getID(), 0,
        )

        """Paso 4: Asignando nuevos jugadores a la mesa"""
        self.mesa.newPlayer(self.jugadores[0])
        self.mesa.newPlayer(self.jugadores[1])


if '__main__' == __name__:
    unittest.main()
