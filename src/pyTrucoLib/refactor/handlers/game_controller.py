from itertools import cycle
from controller import Controler
from ...jugador import Jugador
from ...team import Team

t1 = Team(0)
t2 = Team(1)
j1 = Jugador(0)
j1.setTeam(t1)
j2 = Jugador(0)
j2.setTeam(t2)

class game_controller(Controler):

    def __init__(self):
        self.teams = {t1, t2}
        self.players = [j1, j2]
        self.turn_manager = cycle(self.players)

    def start(self):
        pass
    
    def search_winner(self) -> bool:
        return super().search_winner()