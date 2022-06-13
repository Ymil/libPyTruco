from abc import ABC
from typing import Union


class Results(ABC):
    pass


class Controler(ABC):
    def start(self) -> None:
        raise NotImplementedError

    def search_winner(self, *args) -> Union[Results, bool]:
        raise NotImplementedError
