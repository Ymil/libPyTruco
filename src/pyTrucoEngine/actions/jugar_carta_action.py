from pyTrucoEngine.actions.action import Action


class jugar_carta(Action):

    def get_availables_actions(self):
        self._availables_next_actions = self.from_action.get_availables_actions()  # noqa
        return self._availables_next_actions

    def execute(self, action_value):
        if action_value is None:
            raise ValueError('Se debe ingresar el indice de la carta')
        card_idx = int(action_value)
        if(not self.player.playing_card(card_idx)):
            self.GM.signals.showError(
                self.player,
                'cardPlayerd',
            )
            return self.get_action(self, self.player)

        self.GM.signals.showCardPlaying(
            self.player.getTeam(),
            self.player,
            self.player.getNameCardPlayed(),
        )

        self.GM.hand.playing_card(self.player, self.player.cartas[card_idx])
        if(len(self.GM.hand._played_cards) >= len(self.GM.game.players)):
            return ('hand_finish', self.player, None)
        return super().execute(action_value)
