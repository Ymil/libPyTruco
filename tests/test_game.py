import xml.etree.ElementTree as ET
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

        tree = ET.parse('tests/game.xml')
        self.root = tree.getroot()
        self.rounds_cards = self.root.iter('round')
        self.commands = self.root.iter("command")

    
    def get_action(self, *args):
        return next(self.commands).text
    
    def give_cards(self, *args):
        round = next(self.rounds_cards)
        for cards in round.findall("cards"):
            _cards = list(map(lambda x: Card(x.text), cards.findall("card")))
            player = self.GM.game.players[int(cards.attrib['player'])]
            self.GM.signals.giveCards(player.getID(), _cards)
            self.GM.signals.showCards(player, _cards)
            player.setCards(_cards)

    @mock.patch(
        'pyTrucoLib.handlers.signals.signals.get_action',
    )
    @mock.patch(
        'pyTrucoLib.controllers.round_controller.round_controller.give_cards',
    )
    def test_simulate_game(self, give_cards, get_action):
        """
            Se simula un juego real y se espera que no falle
        """
        get_action.side_effect = self.get_action
        give_cards.side_effect = self.give_cards
        self.game.start()
    

