from controller import Controler

class hand_controller(Controler):
    _played_cards = []
    def __init__(self, game_controller):
        self._game_controller = game_controller
    
    def start(self):
        # get_action()
        pass

    def playing_card(self, player, card):
        self._played_cards.append((player, card))
    
    def search_winner(self) -> dict:
        '''Devuelve el ganador de la ultima mano

        :return: {playerObject, bool}
        :rtype: dic
        '''

        tempResultHand = {
            'player': None,
            'card': None,
            'parda': False,
        }
        # Resultado temporal de la mano
        for player, card in self._played_cards:
            # No concuerda con la mano, falta terminar esto.

            if tempResultHand['player'] is not None:
                tempCardWin = tempResultHand['card']
            else:
                '''Esta exception se captura cuando todavia
                no hay un jugador en
                el resultado ganador'''
                tempCardWin = 0

            if tempCardWin < card:
                tempResultHand['player'] = player
                tempResultHand['parda'] = False
            elif tempCardWin == card:
                # Hay una parda
                tempResultHand['parda'] = True

        return tempResultHand
