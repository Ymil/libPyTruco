from abc import ABC
from controller import Controler
from pyTrucoLib.cartas import Cartas
from pyTrucoLib.refactor.handlers.game_controller import game_controller
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
    quiero_player: str = None
    cantado: bool = False
    quiero_expected = False


class envido_manager(points_manager):
    cantado: bool = True


class round_controller(Controler):
    _current_hand = 0
    game = None

    def __init__(self, game_controller):
        self.game = game_controller
        self._truco_manager = truco_manager()
        self._envido_manager = envido_manager()

    def give_cards(self):
        cards = Cartas()
        for player in self.game.players:
            
            cardsPlayer = cards.repartir_individual()
            # self.table.signals_handler.giveCards(player.getID(), cardsPlayer)
            player.setCards(cardsPlayer)
            # self.table.signals_handler.showCards(player, cardsPlayer)
            print(f'{player} cartas: {cardsPlayer}')

    def start(self):
        self.give_cards()

        first_hand = hand_controller(
            self.game,
            self
        )
        first_hand.start()
        result_first_hand = first_hand.search_winner()
        del first_hand
        if result_first_hand["finish_round"]:
            return

        second_hand = hand_controller(
            self.game,
            self
        )
        second_hand.start()
        result_second_hand = second_hand.search_winner()
        del second_hand
        if result_first_hand["finish_round"]:
            return
        else:
            if result_first_hand["player"] == result_second_hand["player"]:
                print(f"Ganador {result_second_hand['player']}")
                return
            if result_first_hand["parda"] and not result_second_hand["parda"]:
                print(f"Ganador {result_second_hand['player']}")
                return
            elif result_second_hand["parda"]:
                print(f"Ganador {result_first_hand['player']}")
                return

        third_hand = hand_controller(
            self.game,
            self
        )
        third_hand.start()
        result_third_hand = third_hand.search_winner()
        if result_third_hand["finish_round"]:
            return
        else:
            if result_second_hand["player"] == result_third_hand["player"]:
                print(f"Ganador {result_third_hand['player']}")
                return
            if result_second_hand["parda"] and not result_third_hand["parda"]:
                print(f"Ganador {result_third_hand['player']}")
                return
            elif result_third_hand["parda"]:
                print(f"Ganador {result_third_hand['player']}")
                return


        if self.search_winner():
            return True

    def search_winner(self) -> bool:
        return super().search_winner()

if __name__ == "__main__":
    gc = game_controller()
    rc = round_controller(gc)
    rc.start()