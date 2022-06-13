from unittest import TestCase

from pyTrucoEngine.card import Card
from pyTrucoEngine.player import Player


class test_envido_points(TestCase):
    def setUp(self):
        self.player = Player(0)

    def test_envido_flor(self):
        """
            Se verifica que los puntos del envido sean correctos cuando
            hay flor
        """
        self.player.setCards(
            [Card('3_oro'), Card('4_oro'), Card('12_oro')],
        )

        self.assertEqual(
            self.player.getPointsEnvido(), 27,
        )

        self.player.setCards(
            [Card('3_oro'), Card('4_oro'), Card('7_oro')],
        )

        self.assertEqual(
            self.player.getPointsEnvido(), 31,
        )

        self.player.setCards(
            [Card('3_oro'), Card('11_oro'), Card('12_oro')],
        )

        self.assertEqual(
            self.player.getPointsEnvido(), 23,
        )

        self.player.setCards(
            [Card('10_oro'), Card('11_oro'), Card('12_oro')],
        )

        self.assertEqual(
            self.player.getPointsEnvido(), 20,
        )
