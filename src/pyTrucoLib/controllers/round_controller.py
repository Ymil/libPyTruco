from abc import ABC
from dataclasses import dataclass

from ..cartas import Cartas
from .controller import Controler
from .hand_controllers import hand_controller

HAND_CONTROLLERS = []


class points_manager(ABC):
    _points: int = 0

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value


class truco_manager(points_manager):
    start_player: str = None
    quiero_player: str = None
    cantado: bool = False
    quiero_expected = False
    _points: int = 1
    next_availables_actions = set()


class envido_manager(points_manager):
    cantado: bool = False
    start_player: str = None


@dataclass
class round_result:
    player: int = None
    team: int = None


class round_controller(Controler):
    _current_hand = 0
    game = None

    def __init__(self, game_mediator):
        self.GM = game_mediator
        self.truco_manager = truco_manager()
        self.envido_manager = envido_manager()
        self.GM.set_round(self)

    def give_cards(self):
        cards = Cartas()
        for player in self.GM.game.players:
            cardsPlayer = cards.repartir_individual()
            self.GM.signals.giveCards(player.getID(), cardsPlayer)
            player.setCards(cardsPlayer)
            self.GM.signals.showCards(player, cardsPlayer)

    def start(self):
        self.GM.signals.start_new_round()

        self.give_cards()

        player_winner = None

        start_player_round = self.GM.turn_manager.next_without_changes()
        """
            Se inicia la primera mano
        """
        first_hand = hand_controller(
            self.GM,
            1,
        )
        first_hand.start()
        result_first_hand = first_hand.search_winner()
        if result_first_hand.finish_round:
            return round_result(
                result_first_hand.player,
                result_first_hand.player.getTeam(),
            )
        elif result_first_hand.player:
            self.GM.turn_manager.set_next(
                result_first_hand.player,
            )
        elif result_first_hand.parda:
            self.GM.turn_manager.set_next(
                start_player_round,
            )

        self.showPointsTeams()

        """
            Se inicia la segunda mano
        """
        second_hand = hand_controller(
            self.GM,
            2,
        )
        second_hand.start()
        result_second_hand = second_hand.search_winner()
        if result_second_hand.finish_round:
            return round_result(
                result_second_hand.player,
                result_second_hand.player.getTeam(),
            )
        else:
            if result_first_hand.player == result_second_hand.player:
                player_winner = result_second_hand.player
            elif result_first_hand.parda and not result_second_hand.parda:
                player_winner = result_second_hand.player
            elif result_second_hand.parda:
                player_winner = result_first_hand.player

            if(self.search_winner(player_winner)):
                return round_result(
                    player_winner,
                    player_winner.getTeam(),
                )

        if result_second_hand.player:
            self.GM.turn_manager.set_next(
                result_second_hand.player,
            )
        elif result_second_hand.parda:
            self.GM.turn_manager.set_next(
                start_player_round,
            )

        """
            Se inicia la tercera mano
        """
        third_hand = hand_controller(
            self.GM,
            3,
        )
        third_hand.start()
        result_third_hand = third_hand.search_winner()
        if result_third_hand.finish_round:
            return round_result(
                result_second_hand.player,
                result_second_hand.player.getTeam(),
            )
        else:
            if result_second_hand.parda and not result_third_hand.parda:
                player_winner = result_third_hand.player
            elif result_second_hand.parda and result_third_hand.parda:
                player_winner = start_player_round
            elif result_third_hand.parda:
                player_winner = result_second_hand.player
            elif result_second_hand.player == result_third_hand.player:
                player_winner = result_third_hand.player
            else:
                player_winner = result_third_hand.player

            if(self.search_winner(player_winner)):
                return round_result(
                    player_winner,
                    player_winner.getTeam(),
                )

    def showPointsTeams(self):
        ''' Muestra los puntos de los equipos '''
        for team in self.GM.game.teams:
            self.GM.signals.show_points_for_team(
                team.getID(), team.getPoints(),
            )

    def search_winner(self, player_winner) -> bool:
        if player_winner is not None:
            player_winner.getTeam().givePoints(self.GM.truco_manager.points)
            self.GM.signals.win(player_winner.getTeamID())
            self.showPointsTeams()
            return True
        self.showPointsTeams()
        return False
