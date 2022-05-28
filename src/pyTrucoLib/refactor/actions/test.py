



from abc import ABC
from itertools import cycle
from pyTrucoLib.refactor.actions.envido_actions import *
from pyTrucoLib.refactor.actions.pyTrucoLib.refactor.actions.functions import get_action
from pyTrucoLib.refactor.actions.truco_actions import *
from pyTrucoLib.refactor.actions.jugar_carta_action import jugar_carta
from pyTrucoLib.refactor.actions.functions import *

players = cycle(["player1", "player2"])



class round:


class game:
    turn_manager = players

        


def main():
    player = next(players)
    get_action(
        initial_action(game(), round(), get_action, player), 
        player
    )

main()