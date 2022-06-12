__author__ = 'Lautaro Linquiman'
__email__ = 'acc.limayyo@gmail.com'
__status__ = 'Developing'
__date__ = ' 04/08/16'
from abc import ABC
import logging


class signals(ABC):
    '''
    Esta clase almacena los eventos que se disparan a medida que se
    va ejecuntado el juego.

    Como mostrar mensajes, dar cartas etc.

    Esta clase es de ejemplo
    '''

    players: list = []
    teams = []

    def __init__(self, players):
        self.errors = {
            'cardPlayerd': 'Esta carta ya fue jugada',
            'invalidAction': 'No puedes realizar esta accion',
        }
        self.players = players

    def showMsgStartGame(self):
        ''' Esta funcion se dispara cuando se inicia un nuevo juego
        :param players:
        '''
        pass

    def sendMessageAll(self, msg):
        print(msg)
        # for player in self.players:
        # self.sendMessageToPlayer(player, msg)

    def sendMessageToPlayer(self, player, msg):
        print(f'{player}: {msg}')

    def start_new_round(self):
        ''' Esta funcion se dispara cuando se inicia una nueva ronda
        '''
        logging.debug('startRound')

    def start_new_hand(self, handsNumber):
        ''' Esta funcion se llama cada vez que se inicia una nueva mano
        :param handsNumber: int'''
        str1 = ('Iniciando mano %d' % handsNumber).center(50, '-')
        self.sendMessageAll(str1)
        logging.debug('startHand(%d)' % handsNumber)
        logging.info(str1)

    def showMsgFinishHand(self):
        ''' Esta funcion se dispara cuando finaliza una mano
        '''
        logging.debug('finishHand')

    def showMsgFinishRound(self):
        ''' Esta funcion se dispara cuando finaliza una ronda
        '''
        logging.debug('finishRound')

    def showMsgFinishGame(self):
        ''' Esta funcion se dispara cuando finaliza un juego
        '''
        logging.debug('finishGame')

    def giveCards(self, playerid, cards):
        ''' Esta funcion se dispara cuando se reparten las cartas,
        recibe como parametro el playerid y las cartas del jugador
        :param playerid:
        :param cards: list cardsObjects
        Ejemplo de uso:
        partida.mostrarCartas(player, cards) '''
        pass

    def showCards(self, player, cards):
        ''' Esta funcion se dispara cuando se le muestran las cartas al jugador
        params
        :param playerid:
        :param cards: list cardsObjects
        '''
        print(f'{player} {cards}')
        pass

    def show_points_for_team(self, team, pointsTeam):
        ''' Esta funcion se dispara cuando se muestran los puntos de los equipos
        :param team: int teamID
        :param pointsTeam: int
        Ejemplo de uso: '''

        str1 = 'El equipo %d tiene %d puntos' % (team, pointsTeam)
        self.sendMessageAll(str1)
        str2 = 'teamPoints(%d,%d)' % (team, pointsTeam)
        logging.debug(str2)
        logging.info(str1)

    def get_action(self, player, actions_availables=''):
        ''' Esta funcion se llama cuando se tiene que obtener un
        accion del jugador


        :param player:
        :param gameInfo: contiene información del juego

        :return:Esta funcion entrega informacion del estado
        juego en la variable infoGame
        :rtype: list


        Ejemplo:
        accion = raw_input("Escriba la accion o carta a jugar>")
        return accion(accion, valorAccion)

        Acciones[JugadorCarta, envido, real envido,
         falta envido, truco, re truco, vale 4]

        formato de respuesta: (accion, valor)
        '''

        ''' Las siguientes funciones generan jugadas de forma aleatoria
        para debuggiar el sistema. '''
        print(player, ' ', actions_availables)
        return input('>')

    def showCardPlaying(self, teamObject, player, cardObject):
        ''' Esta funcion se llama cuando se juega una carta
        :param teamObject:
        :param player:
        :param cardObject:
        Ejemplo:
        '''
        str1 = 'El jugador %d:%d jugo la carta %s' % (
            teamObject.getID(), player.getID(), cardObject.getText(),
        )
        self.sendMessageAll(str1)
        logging.info(str1)
        str2 = 'showCardPlaying(%d,%d,%s)' % (
            teamObject.getID(), player.getID(), cardObject.getText(),
        )
        logging.debug(str2)

    def showError(self, player, errorName):
        ''' Esta funcion se llama cuando ocurre un error por un jugador
        :param player:
        :param errorName: str ['cardPlayerd', 'invalidAction']
        Ejemplo:
        '''
        self.sendMessageToPlayer(player, errorName)
        # self.sendMessageAll(self.errors[errorName])
        pass

    def showResultaTheHand(self, playerid, playername, teamid, cardObject):
        ''' Esta funcion se llama cuando termina una mano

        :param playerid: int
        :param playername: str Nombre del jugador
        :param teamid: int
        :param cardObject:
        Ejemplo:'''
        str1 = '%d:%d gano la mano con %s' % (
            teamid, playerid, cardObject.getText(),
        )
        self.sendMessageAll(str1)
        logging.info(str1)
        str2 = 'showResultaTheHand(%d,%d,%s)' % (
            teamid, playerid, cardObject.getText(),
        )
        logging.debug(str2)

    def returnStatus(self, statusGame):
        ''' Esta funcion se llama cada vez que se busca un ganador
        :param statusGame: [StatusGame=(win,empate), teamWinner],
         [StatusGame=empate, CartaMayor],
         [StatusGame=continue, CartaMayor, playerid]
        '''
        # logging.debug("ReturnStatus")
        # self.sendMessageAll('Status:',statusGame)
        pass

    ''' Win Actions '''

    def winEmpate(self, teamIDWinner):
        ''' Esta funcion se llama cuando ocurre un empate

        :param teamIDWinner: int
        '''
        str1 = 'Ocurrio un empate, los puntos son para el ' \
            f'equipo {teamIDWinner}'
        self.sendMessageAll(str1)
        logging.info(str1)

    def win(self, teamIDWinner):
        ''' Esta funcion se llama cuando se gana la ronda

        :param teamIDWinner: int
        '''
        str1 = 'El equipo %s gano la ronda' % teamIDWinner
        self.sendMessageAll(str1)
        logging.info(str1)

    def winGameTeam(self, teamObject):
        ''' Esta funcion se llama cuando un equipo gana el juego

        :param teamObject:
        '''
        str1 = 'El equipo %d gano el juego' % teamObject.getID()
        self.sendMessageAll(str1)
        logging.info(str1)

    ''' Start quiero/Noquiero '''

    def quiero(self, player):
        ''' Esta funcion se llama cuando un jugador quiere a un canto

        :param player:
        '''

        str1 = f'{player} dijo quiero'
        self.sendMessageAll(str1)

    def noquiero(self, player):
        ''' Esta funcion se llama cuando un jugador no quiere a un canto

        :param player:
        '''

        str1 = f'{player} dijo no quiero'
        self.sendMessageAll(str1)

    ''' Finish quiero/Noquiero '''

    def envido(self, player):
        '''
        Esta funcion se llama cuando alguien canta envido
        :param player:
        '''
        str1 = 'El jugador %d canto envido' % player.getID()
        self.sendMessageAll(str1)

    def real_envido(self, player):
        '''
        Esta funcion se llama cuando alguien canta envido
        :param player:
        '''
        str1 = 'El jugador %d canto real envido' % player.getID()
        str2 = 'envido(%d)' % player.getID()
        self.sendMessageAll(str1)

    def falta_envido(self, player):
        '''
        Esta funcion se llama cuando alguien canta envido
        :param player:
        '''
        str1 = 'El jugador %d canto falta envido' % player.getID()
        self.sendMessageAll(str1)

    def showEnvido(self, player):
        '''
        Esta funcion se llama cuando un jugar canta su envido
        :param player: '''
        str1 = 'El jugador %d tiene %d de envido' % (
            player.getID(), player.getPointsEnvido(),
        )
        str2 = 'showEnvido(%d,%d)' % (
            player.getID(),
            player.getPointsEnvido(),
        )
        self.sendMessageAll(str1)
        logging.info(str1)
        logging.debug(str2)

    def showWinnerEnvido(self, team):
        '''
        Esta funcion se llama cuando se define un ganador del envido
        :param player:
        '''

        str1 = 'El equipo %d gano el envido' % team.getID()
        self.sendMessageAll(str1)

    def truco(self, player):
        str1 = f'{player} canto truco'
        self.sendMessageAll(str1)

    def retruco(self, player):
        str1 = f'{player} canto re truco'
        self.sendMessageAll(str1)

    def vale_4(self, player):
        str1 = f'{player} canto vale 4'
        self.sendMessageAll(str1)
