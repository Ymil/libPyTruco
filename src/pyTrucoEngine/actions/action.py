from abc import ABC
from dataclasses import dataclass
from dataclasses import InitVar
from typing import Any
from typing import Set

from ..player import Player


@dataclass
class Action(ABC):
    from_action: Any
    player: Player
    _availables_next_actions: InitVar[Set] = {}

    def __post_init__(self, *args):
        self.GM = self.from_action.GM

    def get_availables_actions(self):
        return self._availables_next_actions

    def get_availables_actions_str(self):
        return list(
            map(lambda c: c.name(), self.get_availables_actions()),
        )

    def get_action_from_name(self, name):
        return list(self._availables_next_actions)[
            self.get_availables_actions_str().index(name)
        ]

    def execute(self, action_value):
        next_player = next(self.GM.turn_manager)
        return self.GM.get_action(self, next_player)

    @classmethod
    def name(cls):
        return cls.__name__
