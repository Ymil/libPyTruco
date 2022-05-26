from controller import Controler

HAND_CONTROLLERS = [

]

class round_controller(Controler):
    _current_hand = 0
    _game_controller = None
    def __init__(self, game_controller):
        self._game_controller = game_controller
    
    def start(self):
        HAND_CONTROLLERS[self._current_hand](

        )

        if self.search_winner():
            return True

    def search_winner(self) -> bool:
        return super().search_winner()
    
