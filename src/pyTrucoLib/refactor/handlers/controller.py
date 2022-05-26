from abc import ABC


class Controler(ABC):
    def start(self) -> None:
        raise NotImplementedError

    def search_winner(self) -> bool:
        raise NotImplementedError