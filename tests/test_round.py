from unittest import mock
from unittest import TestCase

from pyTrucoLib.card import Card
from pyTrucoLib.controllers.game_controller import game_controller
from pyTrucoLib.controllers.round_controller import round_controller
from pyTrucoLib.handlers.signals import signals
from pyTrucoLib.player import Player
from pyTrucoLib.table import Table


def give_cards(game_mediator, cards_player_one, cards_player_two):
    GM = game_mediator
    player_one = GM.game.players[0]
    cards = list(map(lambda card: Card(card), cards_player_one))
    GM.signals.giveCards(player_one.getID(), cards)
    GM.signals.showCards(player_one, cards)
    player_one.setCards(cards)

    cards = list(map(lambda card: Card(card), cards_player_two))
    player_two = GM.game.players[1]
    GM.signals.giveCards(player_two.getID(), cards)
    GM.signals.showCards(player_two, cards)
    player_two.setCards(cards)


@mock.patch(
    'pyTrucoLib.controllers.round_controller.round_controller.give_cards',
    return_value=None,
)
class test_hand(TestCase):
    def setUp(self):
        """ Paso 1: Definiendo parametros de la simulacion """
        self.cantidadDeJugadores = 2

        """Paso 2: Definiendo jugadores"""
        self.jugadores = []
        self.jugadores.append(Player(1))
        self.jugadores.append(Player(2))

        """ Paso : Creando mesa """
        self.mesa = Table(
            self.cantidadDeJugadores,
            self.jugadores[0].getID(), 0,
        )

        """Paso 4: Asignando nuevos jugadores a la mesa"""
        self.mesa.newPlayer(self.jugadores[0])
        self.mesa.newPlayer(self.jugadores[1])

        self.game = game_controller(
            set(self.mesa.getTeams()),
            self.mesa.getPlayers(),
            signals(self.mesa.getPlayers()),
        )

        self.GM = self.game.GM

    @mock.patch(
        'pyTrucoLib.handlers.signals.signals.get_action',
        side_effect=[
            ('jugar_carta,0'),
            ('jugar_carta,0'),
            ('jugar_carta,1'),
            ('jugar_carta,1'),
        ],
    )
    def test_round_parda_1(self, *args):
        """
            Probando la busqueda de pardas
        """
        give_cards(
            self.GM,
            cards_player_one=[
                [3, 'oro', 10], [
                3, 'espada', 10,
                ], [1, 'oro', 8],
            ],
            cards_player_two=[
                [3, 'basto', 10], [
                7, 'oro', 11,
                ], [1, 'espada', 14],
            ],
        )

        round = round_controller(self.GM)
        result = round.start()
        self.assertEqual(result.player, self.GM.game.players[1])

    @mock.patch(
        'pyTrucoLib.handlers.signals.signals.get_action',
        side_effect=[
            ('jugar_carta,0'),
            ('jugar_carta,0'),
            ('jugar_carta,1'),
            ('jugar_carta,1'),
            ('jugar_carta,2'),
            ('jugar_carta,2'),
        ],
    )
    def test_round_parda_2(self, *args):
        """
            Probando la busqueda de pardas
        """
        give_cards(
            self.GM,
            cards_player_one=[
                [3, 'oro', 10], [
                3, 'espada', 10,
                ], [1, 'oro', 8],
            ],
            cards_player_two=[
                [3, 'basto', 10], [
                3, 'copa', 10,
                ], [1, 'espada', 14],
            ],
        )

        round = round_controller(self.GM)
        result = round.start()
        self.assertEqual(result.player, self.GM.game.players[1])

    @mock.patch(
        'pyTrucoLib.handlers.signals.signals.get_action',
        side_effect=[
            ('jugar_carta,0'),
            ('jugar_carta,0'),
            ('jugar_carta,1'),
            ('jugar_carta,1'),
            ('jugar_carta,2'),
            ('jugar_carta,2'),
        ],
    )
    def test_round_parda_3(self, *args):
        """
            Probando la busqueda de pardas
        """
        give_cards(
            self.GM,
            cards_player_one=[
                [3, 'oro', 10], [
                3, 'espada', 10,
                ], [10, 'basto', 5],
            ],
            cards_player_two=[
                [3, 'basto', 10], [
                3, 'copa', 10,
                ], [10, 'copa', 5],
            ],
        )

        round = round_controller(self.GM)
        result = round.start()
        self.assertEqual(result.player, self.GM.game.players[0])

    @mock.patch(
        'pyTrucoLib.handlers.signals.signals.get_action',
        side_effect=[
            ('truco'),
            ('no_quiero'),
        ],
    )
    def test_round_truco_no_quiero_1(self, *args):
        """
            Probando la busqueda de pardas
        """
        give_cards(
            self.GM,
            cards_player_one=[
                [3, 'oro', 10], [
                3, 'espada', 10,
                ], [10, 'basto', 5],
            ],
            cards_player_two=[
                [3, 'basto', 10], [
                3, 'copa', 10,
                ], [10, 'copa', 5],
            ],
        )

        round = round_controller(self.GM)
        result = round.start()
        self.assertEqual(result.player, self.GM.game.players[0])

    @mock.patch(
        'pyTrucoLib.handlers.signals.signals.get_action',
        side_effect=[
            ('jugar_carta,0'),
            ('jugar_carta,2'),
            ('truco'),
            ('no_quiero'),
        ],
    )
    def test_round_truco_no_quiero_1(self, *args):
        """
            Probando la busqueda de pardas
        """
        give_cards(
            self.GM,
            cards_player_one=[
                [3, 'oro', 10], [
                3, 'espada', 10,
                ], [10, 'basto', 5],
            ],
            cards_player_two=[
                [3, 'basto', 10], [
                3, 'copa', 10,
                ], [10, 'copa', 5],
            ],
        )

        round = round_controller(self.GM)
        result = round.start()
        self.assertEqual(result.player, self.GM.game.players[0])
