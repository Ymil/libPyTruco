from abc import ABC, abstractmethod
from copy import copy
from dataclasses import InitVar, dataclass, field
from itertools import cycle
from typing import List
players = cycle(["player1", "player2"])

@dataclass
class Action(ABC):
    from_action: str
    player: str
    truco_manager: str = field(init=False)
    envido_manager:str = field(init=False)
    _availables_next_actions: InitVar[List] = []

    def __post_init__(self, *args):
        self.truco_manager = self.from_action.truco_manager
        self.envido_manager = self.from_action.envido_manager

    def get_availables_actions(self):
        return self._availables_next_actions

    def get_availables_actions_str(self):
        return list(
            map(lambda c: c.name(), self.get_availables_actions())
        )
    
    def get_action_from_name(self, name):
        return self._availables_next_actions[
            self.get_availables_actions_str().index(name)
        ]

    def execute(self, action_value):
        print(self)
        next_player = next(players)
        get_action(self, next_player)
    
    @classmethod
    def name(cls):
        return cls.__name__

def get_action(action: Action, player) -> None:
    print(player, action.get_availables_actions_str())    
    action_name, action_value = input("").split(",")
    if(action_name in action.get_availables_actions_str()):
        new_action = action.get_action_from_name(action_name)
        action = new_action(action, player)
        action.execute(action_value)
    else:
        get_action(action, player)


class quiero_truco(Action):
    @classmethod
    def name(cls):
        return "quiero"

    def execute(self, *args):
        self.truco_manager.quiero_player = self.player
        if isinstance(self.from_action, truco):
            self._availables_next_actions = [
                jugar_carta, re_truco
            ]
        elif isinstance(self.from_action, re_truco):
            self._availables_next_actions = [
                jugar_carta, vale_4
            ]
        elif isinstance(self.from_action, vale_4):
            self._availables_next_actions = [
                jugar_carta
            ]
        return super().execute(*args)

class no_quiero_truco(Action):
    @classmethod
    def name(cls):
        return "no_quiero"

DEFAULT_TRUCO_ACTIONS = [
    quiero_truco, no_quiero_truco
]

class vale_4(Action):
    _availables_next_actions = DEFAULT_TRUCO_ACTIONS

    def execute(self, action_value):
        self.truco_manager.points = 4
        return super().execute(action_value)

class re_truco(Action):
    _availables_next_actions = [
         vale_4
    ] + DEFAULT_TRUCO_ACTIONS

    def execute(self, action_value):
        self.truco_manager.points = 3
        return super().execute(action_value)


class truco(Action):
    _availables_next_actions = [
        re_truco
    ] + DEFAULT_TRUCO_ACTIONS

    def execute(self, action_value):
        self.truco_manager.points = 2
        self.truco_manager.cantado = True
        return super().execute(action_value)

class jugar_carta(Action):
    def get_availables_actions(self):
        self._availables_next_actions = self.from_action.get_availables_actions()
        return self._availables_next_actions

class quiero_envido(Action):
    _availables_next_actions = [
        jugar_carta, truco
    ]

    @classmethod
    def name(cls):
        return "quiero"

class no_quiero_envido(Action):
    _availables_next_actions = [
        jugar_carta, truco
    ]
    @classmethod
    def name(cls):
        return "no_quiero"

DEFAULT_ENVIDO_ACTIONS = [
    quiero_envido, no_quiero_envido
]

class falta_envido(Action):
    _availables_next_actions = DEFAULT_ENVIDO_ACTIONS

class real_envido(Action):
    _availables_next_actions = [
        falta_envido
    ] + DEFAULT_ENVIDO_ACTIONS

    def execute(self, action_value):
        self._availables_next_actions.append(self)
        return super().execute(action_value)
        

class envido(Action):
    _availables_next_actions = [
        real_envido, falta_envido
    ] + DEFAULT_ENVIDO_ACTIONS

    def execute(self, action_value):
        self._availables_next_actions.append(self)
        return super().execute(action_value)

class points_manager(ABC):
    _points: int = 0

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        print("setter of x called")
        self._points = value

class truco_manager(points_manager):
    quiero_player: str = None
    cantado: bool = False

class envido_manager(points_manager):
    cantado: bool = True

class round:
    _truco_manager = truco_manager()
    _envido_manager = envido_manager()

class initial_action(Action):
    _availables_next_actions = [
        jugar_carta, truco, envido, real_envido, falta_envido
    ]

    def __init__(self, round, player):
        self.from_action = None
        self.truco_manager = round._truco_manager
        self.envido_manager = round._envido_manager
        self.player = player
        

def main():
    player = next(players)
    get_action(initial_action(round(), player), player)

main()