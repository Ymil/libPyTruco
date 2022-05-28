from action import Action

class jugar_carta(Action):
    def get_availables_actions(self):
        self._availables_next_actions = self.from_action.get_availables_actions()
        return self._availables_next_actions
