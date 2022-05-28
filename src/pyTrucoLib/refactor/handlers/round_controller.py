from abc import ABC
from controller import Controler
from pyTrucoLib.cartas import Cartas
from pyTrucoLib.refactor.handlers.hand_controllers import hand_controller

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
    cantado: bool = True
    start_player: str = None


class round_controller(Controler):
    _current_hand = 0
    game = None

    def __init__(self, game_controller):
        self.game = game_controller
        self.signals = self.game.signals
        self._truco_manager = truco_manager()
        self._envido_manager = envido_manager()

    def give_cards(self):
        cards = Cartas()
        for player in self.game.players:
            
            cardsPlayer = cards.repartir_individual()
            self.signals.giveCards(player.getID(), cardsPlayer)
            player.setCards(cardsPlayer)
            self.signals.showCards(player, cardsPlayer)
            

    def start(self):
        self.signals.start_new_round()

        self.give_cards()

        player_winner = None

        first_hand = hand_controller(
            self.game,
            self,
            1
        )
        first_hand.start()
        result_first_hand = first_hand.search_winner()
        if result_first_hand["finish_round"]:
            return
        if "player" in result_first_hand:
            self.game.turn_manager.set_next(
                result_first_hand["player"]
            )
        
        self.showPointsTeams()
        second_hand = hand_controller(
            self.game,
            self,
            2
        )
        second_hand.start()
        result_second_hand = second_hand.search_winner()
        if result_first_hand["finish_round"]:
            return
        else:
            if result_first_hand["player"] == result_second_hand["player"]:
                player_winner = result_second_hand['player']
            if result_first_hand["parda"] and not result_second_hand["parda"]:
                player_winner = result_second_hand['player']
            elif result_second_hand["parda"]:
                player_winner = result_first_hand['player']
        
        if "player" in result_first_hand:
            self.game.turn_manager.set_next(
                result_first_hand["player"]
            )
        
        if(self.search_winner(player_winner)):
            return

        third_hand = hand_controller(
            self.game,
            self,
            3
        )
        third_hand.start()
        result_third_hand = third_hand.search_winner()
        if result_third_hand["finish_round"]:
            return
        else:
            if result_second_hand["player"] == result_third_hand["player"]:
                
                player_winner = result_third_hand['player']
            elif result_second_hand["parda"] and not result_third_hand["parda"]:
                player_winner = result_third_hand['player']
            elif result_third_hand["parda"]:
                player_winner = result_first_hand['player']
            else:
                player_winner = result_third_hand['player']
        if(self.search_winner(player_winner)):
            return
    
    def showPointsTeams(self):
        ''' Muestra los puntos de los equipos '''
        for team in self.game.teams:
            self.signals.show_points_for_team(team.getID(), team.getPoints())

    def search_winner(self, player_winner) -> bool:
        if player_winner is not None:
            player_winner.getTeam().givePoints(self._truco_manager.points)
            self.signals.win(player_winner.getTeamID())
            self.showPointsTeams()
            return True
        self.showPointsTeams()
        return False
