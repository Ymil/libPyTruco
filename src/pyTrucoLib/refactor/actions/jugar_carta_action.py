from pyTrucoLib.refactor.actions.action import Action

class jugar_carta(Action):
    def get_availables_actions(self):
        self._availables_next_actions = self.from_action.get_availables_actions()
        return self._availables_next_actions
    
    def execute(self, action_value):
        card_idx = int(action_value)
        if(not self.player.playing_card(card_idx)):
            return self.get_action_func(self, self.player)
        
        self.hand.playing_card(self.player, self.player.cartas[card_idx])
        if(len(self.hand._played_cards) >= len(self.game.players)):
            return ('hand_finish', self.player, None)
        return super().execute(action_value)

