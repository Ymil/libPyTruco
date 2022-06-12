import json

from pyTrucoLib.handlers.signals import signals


class json_signal_adapter(signals):
    def get_action(self, player, action=''):
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'set_turn_player',
                    'payload': {
                        'team': player.team.getID(),
                        'player': player.getID(),
                    },
                },
            ),
        )
        return player.awaitForResponse(player)

    def showCards(self, player, cards):
        """ Esta funcion se dispara cuando se le muestran las cartas al jugador
        params
        :param playerid:
        :param cards: list cardsObjects
        """
        r = {'action': 'showCards', 'payload': {}}
        for pos, card in enumerate(cards):
            r['payload'][pos] = [card.getNumber(), card.getStick()]
        player.sendMessage(str.encode(json.dumps(r)))

    def start_new_hand(self, handsNumber):
        action = {'action': 'start_new_hand', 'payload': handsNumber}
        self.sendMessageAll(json.dumps(action))

    def showCardPlaying(self, teamObject, playerObject, cardObject):
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'showCardPlaying',
                    'payload': {
                        'team': teamObject.getID(),
                        'player': playerObject.getID(),
                        'card': cardObject.getText(),
                    },
                },
            ),
        )

    def win(self, teamIDWinner):
        self.sendMessageAll(
            json.dumps(
                {'action': 'win', 'team': teamIDWinner},
            ),
        )

    def show_points_for_team(self, team, pointsTeam):
        """ Esta funcion se dispara cuando se muestran los puntos de los equipos
        :param team: int teamID
        :param pointsTeam: int
        Ejemplo de uso: """

        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'show_points_for_team',
                    'payload': {'team': team, 'points': pointsTeam},
                },
            ),
        )

    def start_new_round(self):
        self.sendMessageAll(
            json.dumps(
            {'action': 'start_new_round', 'payload': 0},
            ),
        )

    def showResultaTheHand(self, playerid, playername, teamid, cardObject):
        """ Esta funcion se llama cuando termina una mano

        :param playerid: int
        :param playername: str Nombre del jugador
        :param teamid: int
        :param cardObject:
        Ejemplo:"""
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'showResultaTheHand',
                    'payload': {
                        'player': playerid,
                        'team': teamid,
                        'card': str(cardObject),
                    },
                },
            ),
        )

    def envido(self, playerObject):
        '''
        Esta funcion se llama cuando alguien canta envido
        :param playerObject:
        '''
        str_ = f'El jugador {playerObject.getID()}T{playerObject.team.getID()} canto envido'
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'msg',
                    'payload': str_,
                },
            ),
        )

    def real_envido(self, playerObject):
        '''
        Esta funcion se llama cuando alguien canta envido
        :param playerObject:
        '''
        str_ = f'El jugador {playerObject.getID()}T{playerObject.team.getID()} canto real envido'
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'msg',
                    'payload': str_,
                },
            ),
        )

    def falta_envido(self, player):
        '''
        Esta funcion se llama cuando alguien canta envido
        :param playerObject:
        '''
        str_ = f'El jugador {playerObject.getID()}T{playerObject.team.getID()} canto falta envido'
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'msg',
                    'payload': str_,
                },
            ),
        )

    def showEnvido(self, playerObject):
        '''
        Esta funcion se llama cuando un jugar canta su envido
        :param playerObject: '''
        str_ = f'El jugador {playerObject.getID()}T{playerObject.team.getID()} tiene {playerObject.getPointsEnvido()} de envido'
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'msg',
                    'payload': str_,
                },
            ),
        )

    def showWinnerEnvido(self, team):
        '''
        Esta funcion se llama cuando se define un ganador del envido
        :param playerObject:
        '''

        str_ = f'El equipo {team.getID()} gano el envido'
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'msg',
                    'payload': str_,
                },
            ),
        )

    def quiero(self, playerObject):
        ''' Esta funcion se llama cuando un jugador quiere a un canto

        :param playerObject:
        '''

        str_ = f'El jugador {playerObject.getID()}T{playerObject.team.getID()} dijo quiero'
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'msg',
                    'payload': str_,
                },
            ),
        )

    def noquiero(self, playerObject):
        ''' Esta funcion se llama cuando un jugador no quiere a un canto

        :param playerObject:
        '''

        str_ = f'El jugador {playerObject.getID()}T{playerObject.team.getID()} dijo no quiero'
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'msg',
                    'payload': str_,
                },
            ),
        )

    def truco(self, player):
        str_ = f'El jugador {player.getID()}T{player.team.getID()} canto truco'
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'msg',
                    'payload': str_,
                },
            ),
        )

    def retruco(self, player):
        str_ = f'El jugador {player.getID()}T{player.team.getID()} canto retruco'
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'msg',
                    'payload': str_,
                },
            ),
        )

    def vale_4(self, player):
        str_ = f'El jugador {player.getID()}T{player.team.getID()} canto vale 4'
        self.sendMessageAll(
            json.dumps(
                {
                    'action': 'msg',
                    'payload': str_,
                },
            ),
        )
