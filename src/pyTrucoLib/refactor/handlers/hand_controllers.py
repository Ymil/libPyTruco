from dataclasses import InitVar, dataclass
from typing import List
from controller import Controler
from pyTrucoLib.refactor.actions.functions import get_action
from pyTrucoLib.refactor.actions.initial_action import initial_action
@dataclass
class hand_controller(Controler):
    game: str
    round: str
    _played_cards : InitVar[List] = []
    _signal : InitVar[List] = []
    
    def __post_init__(self, *args):
        self._played_cards = []

    def start(self):
        print("Iniciando mano")
        player = next(self.game.turn_manager)
        self._signal = get_action(initial_action(
            self.game,
            self.round,
            self,
            get_action, 
            player
        ), player)        

    def playing_card(self, player, card):
        self._played_cards.append((player, card))
    
    def search_winner(self) -> dict:
        tempResultHand = {
            'player': None,
            'team': None,
            'card': None,
            'parda': False,
            'finish_round': False
        }
        if self._signal[0] == "hand_finish":
            # Resultado temporal de la mano
            tempCardWin = 0
            for player, card in self._played_cards:
                # No concuerda con la mano, falta terminar esto.

                if tempCardWin == 0:
                    tempCardWin = card.getValue()
                    continue
                card_value = card.getValue()
                if tempCardWin < card_value:
                    tempResultHand['player'] = player
                    tempResultHand['parda'] = False
                elif tempCardWin == card_value:
                    # Hay una parda
                    tempResultHand['parda'] = True

            return tempResultHand
        if self._signal[0] == "truco_no_quiero":
            tempResultHand["finish_round"] = True
            return tempResultHand
            


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