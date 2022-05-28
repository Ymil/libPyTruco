from abc import ABC, abstractmethod
from copy import copy
from dataclasses import InitVar, dataclass, field
from itertools import cycle
from typing import List, Set

players = cycle(["player1", "player2"])

@dataclass
class Action(ABC):
    from_action: str
    player: str
    truco_manager: str = field(init=False)
    envido_manager:str = field(init=False)
    get_action_func:str = field(init=False)
    game:str = field(init=False)
    _availables_next_actions: InitVar[Set] = {}

    def __post_init__(self, *args):
        self.truco_manager = self.from_action.truco_manager
        self.envido_manager = self.from_action.envido_manager
        self.get_action_func = self.from_action.get_action_func
        self.game = self.from_action.game

    def get_availables_actions(self):
        return self._availables_next_actions

    def get_availables_actions_str(self):
        return list(
            map(lambda c: c.name(), self.get_availables_actions())
        )
    
    def get_action_from_name(self, name):
        return list(self._availables_next_actions)[
            self.get_availables_actions_str().index(name)
        ]

    def execute(self, action_value):
        print(self)
        next_player = next(self.game.turn_manager)
        self.get_action_func(self, next_player)
    
    @classmethod
    def name(cls):
        return cls.__name__
