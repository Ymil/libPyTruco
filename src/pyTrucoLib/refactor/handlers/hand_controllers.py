from dataclasses import InitVar, dataclass
from itertools import count
from typing import Counter, List
from controller import Controler
from pyTrucoLib.refactor.actions.functions import get_action
from pyTrucoLib.refactor.actions.initial_action import initial_action


@dataclass
class hand_controller(Controler):
    game: str
    round: str
    number: int
    _played_cards: InitVar[List] = []
    _signal: InitVar[List] = []

    def __post_init__(self, *args):
        self._played_cards = []

    def start(self):
        print("Iniciando mano")
        player = next(self.game.turn_manager)
        self._signal = get_action(
            initial_action(self.game, self.round, self, get_action, player), player
        )

    def playing_card(self, player, card):
        self._played_cards.append((player, card))

    def search_parda(self, max_card):
        """
            No soporta pardas en equipos.
        """
        values_cards_list = list(
            map(lambda x: x.getValue(), list(zip(*self._played_cards))[1])
        )

        cnt_cards_maxs = values_cards_list.count(max_card.getValue())

        if(cnt_cards_maxs == 1):
            return False
        return True

    def search_winner(self) -> dict:
        temp_result = {
            "player": None,
            "team": None,
            "card": None,
            "parda": False,
            "finish_round": False,
        }
        if self._signal[0] == "hand_finish":
            player, card = max(self._played_cards, key=lambda x: x[1].getValue())
            if self.search_parda(card):
                temp_result["parda"] = True
            else:
                temp_result["player"] = player
        if self._signal[0] == "truco_no_quiero":
            temp_result["finish_round"] = True
            return temp_result
        return temp_result


if __name__ == "__main__":
    pass
    # gc = game_controller()
    # hc = hand_controller(
    #     gc,
    #     round_controller(gc)
    # )
    # hc.start()
    # hc.search_winner()
    # print(gc.teams)
