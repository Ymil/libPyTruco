from enum import Enum
from itertools import cycle
from controller import Controler
from pyTrucoLib.jugador import Jugador
from pyTrucoLib.team import Team
from round_controller import round_controller

t1 = Team(0)
t2 = Team(1)
j1 = Jugador(0)
j1.setTeam(t1)
j2 = Jugador(0)
j2.setTeam(t2)

class TurnManager:
    def __init__(self, players):
        self.players = players
        self.current_idx = -1
    
    def next(self):
        self.current_idx += 1
        if self.current_idx >= len(self.players):
            self.current_idx = 0
        return self.players[self.current_idx]
    
    def next_without_changes(self):
        idx = self.current_idx + 1
        if idx >= len(self.players):
            idx = 0
        return self.players[idx]

    def set_next(self, player):
        self.current_idx = self.get_index_for_next(player)

    def get_index_for_next(self, player):
        current_idx = self.players.index(player)
        if current_idx == 0:
            current_idx = len(self.players) - 1
        else:
            current_idx -= 1
        return current_idx

    def set_next_from_player(self, player):
        self.set_next(player)
        next(self)

    def get_current(self):
        return self.players[self.current_idx]

    def __next__(self):
        return self.next()

class game_controller(Controler):

    def __init__(self):
        self.teams = {t1, t2}
        self.players = [j1, j2]
        self.turn_manager = TurnManager(self.players)

    def start(self):
        while True:
            print("Iniciando nueva ronda")
            start_player_round = self.turn_manager.next_without_changes()
            round_controller(self).start()
            self.turn_manager.set_next_from_player(start_player_round)
            if(self.search_winner()):
                return "Finish Game"
    
    def search_winner(self) -> bool:
        if len(list(filter(lambda points: points >= 30, list(map(lambda team: team.getPoints(), self.teams))))) == 1:
            return True
        return False
    
if __name__ == "__main__":
    game_controller(

    ).start()