from dataclasses import InitVar, dataclass
from itertools import count
from typing import Counter, List

from .controller import Controler

from ..actions.initial_action import initial_action

class hand_result:
    player = None 
    team = None
    card = None
    parda : bool = False
    finish_round : bool = None

@dataclass
class hand_controller(Controler):
    GM: int
    number: int
    _played_cards: InitVar[List] = []
    _signal: InitVar[List] = []

    def __post_init__(self, *args):
        self._played_cards = []
        self.GM.set_hand(self)

    def start(self):
        self.GM.signals.start_new_hand(self.number)
        player = next(self.GM.turn_manager)
        self._signal = self.GM.get_action(
            initial_action(self.GM, player), player
        )
        self.GM.signals.showMsgFinishHand()

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
        result = hand_result()
        if self._signal[0] == "hand_finish":
            player, card = max(self._played_cards, key=lambda x: x[1].getValue())
            if self.search_parda(card):
                result.parda = True
            else:
                result.player = player
                self.GM.signals.showResultaTheHand(
                    player.getID(),
                    player.getName(),  player.getTeamID(),
                    player.getNameCardPlayed(),
                )
        if self._signal[0] == "truco_no_quiero":
            result.finish_round = True
            result.player = self.GM.truco_manager.start_player
        
        self.GM.signals.returnStatus(result)
        
        return result