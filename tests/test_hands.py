from unittest import mock
from unittest import TestCase

from pyTrucoEngine.card import Card
from pyTrucoEngine.controllers.game_controller import game_controller
from pyTrucoEngine.controllers.hand_controllers import hand_controller
from pyTrucoEngine.controllers.round_controller import round_controller
from pyTrucoEngine.handlers.signals import signals
from pyTrucoEngine.player import Player
from pyTrucoEngine.table import Table


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
        self.mesa.add_player(self.jugadores[0])
        self.mesa.add_player(self.jugadores[1])

        self.game = game_controller(
            set(self.mesa.getTeams()),
            self.mesa.getPlayers(),
            signals(self.mesa.getPlayers()),
        )

        self.GM = self.game.GM

        self.round = round_controller(self.GM)

        give_cards(
            self.GM,
            cards_player_one=['3_oro', '3_espada', '1_oro'],
            cards_player_two=['3_basto', '3_copa', '1_espada'],
        )

    @mock.patch(
        'pyTrucoEngine.handlers.signals.signals.get_action',
        side_effect=[
            ('jugar_carta,0'),
            ('jugar_carta,0'),
            ('jugar_carta,1'),
            ('jugar_carta,1'),
            ('jugar_carta,2'),
            ('jugar_carta,2'),
        ],
    )
    def test_jugar_carta_parda(self, mock):
        """
            Probando la busqueda de pardas
        """
        hand = hand_controller(self.GM, 1)
        hand.start()
        result = hand.search_winner()
        self.assertTrue(result.parda)

        hand = hand_controller(self.GM, 2)
        hand.start()
        result = hand.search_winner()
        self.assertTrue(result.parda)

    @mock.patch(
        'pyTrucoEngine.handlers.signals.signals.get_action',
        side_effect=[('truco'), ('no_quiero')],
    )
    def test_truco_no_quiero(self, mock):
        """
            Probando el truco y el no quiero
        """
        hand = hand_controller(self.GM, 1)
        hand.start()
        result = hand.search_winner()
        self.assertTrue(result.finish_round)

    @mock.patch(
        'pyTrucoEngine.handlers.signals.signals.get_action',
        side_effect=[('truco'), ('re_truco'), ('no_quiero')],
    )
    def test_retruco_no_quiero(self, mock):
        """
            Probando re truco y no quiero
        """
        hand = hand_controller(self.GM, 1)
        hand.start()
        result = hand.search_winner()
        self.assertTrue(result.finish_round)

    @mock.patch(
        'pyTrucoEngine.handlers.signals.signals.get_action',
        side_effect=[('truco'), ('re_truco'), ('vale_4'), ('no_quiero')],
    )
    def test_vale_4_truco_no_quiero(self, mock):
        """
            Probando vale 4 y no quiero
        """

        hand = hand_controller(self.GM, 1)
        hand.start()
        result = hand.search_winner()
        self.assertTrue(result.finish_round)

    @mock.patch(
        'pyTrucoEngine.handlers.signals.signals.get_action',
        side_effect=[
            ('truco'),
            ('quiero'),
            ('jugar_carta,0'),
            ('jugar_carta,0'),
            ('re_truco'),
            ('quiero'),
            ('jugar_carta,1'),
            ('jugar_carta,1'),
            ('vale_4'),
            ('quiero'),
            ('jugar_carta,2'),
            ('jugar_carta,2'),
        ],
    )
    def test_truco_quiero(self, mock):
        """
            Probando truco y el quiero
        """
        give_cards(
            self.GM,
            cards_player_one=['3_oro', '3_espada', '1_oro'],
            cards_player_two=['4_oro', '7_oro', '1_espada'],
        )
        self.assertFalse(self.GM.truco_manager.cantado)
        hand = hand_controller(self.GM, 1)
        hand.start()
        self.assertTrue(self.GM.truco_manager.cantado)
        self.assertEqual(
            self.GM.truco_manager.quiero_player, self.GM.game.players[1],
        )
        self.assertEqual(
            len(list(self.GM.truco_manager.next_availables_actions)), 1,
        )
        self.assertEqual(
            list(self.GM.truco_manager.next_availables_actions)[
                0
            ].name(), 're_truco',
        )
        self.assertEqual(self.GM.truco_manager.points, 2)

        self.GM.turn_manager.set_next(self.GM.game.players[1])

        hand = hand_controller(self.GM, 2)
        hand.start()
        self.assertTrue(self.GM.truco_manager.cantado)
        self.assertEqual(
            self.GM.truco_manager.quiero_player, self.GM.game.players[0],
        )
        self.assertEqual(
            len(list(self.GM.truco_manager.next_availables_actions)), 1,
        )
        self.assertEqual(
            list(self.GM.truco_manager.next_availables_actions)[
                0
            ].name(), 'vale_4',
        )
        self.assertEqual(self.GM.truco_manager.points, 3)

        self.GM.turn_manager.set_next(self.GM.game.players[0])
        hand = hand_controller(self.GM, 3)
        hand.start()
        self.assertTrue(self.GM.truco_manager.cantado)
        self.assertEqual(
            self.GM.truco_manager.quiero_player, self.GM.game.players[1],
        )
        self.assertEqual(
            len(list(self.GM.truco_manager.next_availables_actions)), 0,
        )
        self.assertEqual(self.GM.truco_manager.points, 4)

    @mock.patch(
        'pyTrucoEngine.handlers.signals.signals.get_action',
        side_effect=[
            ('envido'),
            ('real_envido'),
            ('quiero'),
            ('jugar_carta,0'),
            ('jugar_carta,0'),
        ],
    )
    def test_envido_quiero(self, mock):
        """
            Probando envido, real envido y el quiero
        """
        give_cards(
            self.GM,
            cards_player_one=['3_oro', '3_espada', '1_oro'],
            cards_player_two=['4_oro', '7_oro', '1_espada'],
        )
        self.assertFalse(self.GM.envido_manager.cantado)
        hand = hand_controller(self.GM, 1)
        hand.start()
        self.assertTrue(self.GM.envido_manager.cantado)
        self.assertEqual(
            self.GM.envido_manager.start_player, self.GM.game.players[0],
        )
        self.assertEqual(self.GM.envido_manager.points, 5)

    @mock.patch(
        'pyTrucoEngine.handlers.signals.signals.get_action',
        side_effect=[
            ('envido'), ('no_quiero'),
            ('jugar_carta,0'), ('jugar_carta,0'), ],
    )
    def test_envido_no_quiero(self, mock):
        """
            Probando envido y no quiero
        """
        give_cards(
            self.GM,
            cards_player_one=['3_oro', '3_espada', '1_oro'],
            cards_player_two=['4_oro', '7_oro', '1_espada'],
        )
        self.assertFalse(self.GM.envido_manager.cantado)
        hand = hand_controller(self.GM, 1)
        hand.start()
        self.assertTrue(self.GM.envido_manager.cantado)
        self.assertEqual(
            self.GM.envido_manager.start_player, self.GM.game.players[0],
        )
        self.assertEqual(self.GM.envido_manager.points, 1)
