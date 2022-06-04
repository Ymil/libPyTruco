import threading
import time

from pyTrucoLib.handlers.signals import signals
from pyTrucoLib.juego import Game
from pyTrucoLib.jugador import Jugador
from pyTrucoLib.table import Table
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.protocols import basic


class playerCon(basic.LineReceiver, Jugador):
    delimiter = '\n'
    state = ''
    username = ''
    waitData = ''

    def __init__(self, factory, id):
        self.factory = factory
        Jugador.__init__(self, id)

    def dataReceived(self, data):
        self.waitData = data
        # pass

    def connectionLost(self, reason):
        self.factory.players.remove(self)

    def connectionMade(self):
        self.transport.write(b'Bienvenido al PyTruco Argentino\n\r')
        self.state = 'state'
        self.factory.players.append(self)

    def awaitForResponse(self):
        self.waitData = ''
        self.transport.write(b'>')
        while 1:
            if(len(self.waitData) > 0):
                return self.waitData.decode()
            time.sleep(0.5)


class EchoFactory(protocol.Factory, signals):
    id: int = 0

    def startGame(self):
        mesa = Table(2, 1, 0)
        for player in self.players:
            mesa.newPlayer(player)
        juego = Game(mesa, self)
        juego.start()

    def buildProtocol(self, addr):
        r = playerCon(self, self.id)
        self.id += 1
        if self.id == 2:
            # Comenzamos el juego
            threading.Thread(target=self.startGame).start()
        return r

    def sendMessageAll(self, msg):
        for player in self.players:
            player.transport.write(str.encode(f'{msg}\n\r'))

    def sendMessageToPlayer(self, player, msg):
        player.transport.write(str.encode(f'{msg}\n\r'))

    def get_action(self, player, action=''):
        try:
            response = player.awaitForResponse()
            accion_name, accion_value = str(response).split(',')
        except:  # noqa
            return self.get_action(player, action)
        return str(accion_name), int(accion_value.split('\\')[0])

    def showCards(self, player, cards):
        ''' Esta funcion se dispara cuando se le muestran las cartas al jugador
        params
        :param playerid:
        :param cards: list cardsObjects
        '''
        for pos, card in enumerate(cards):
            player.transport.write(str.encode(f'{pos} - {card}\n\r'))


reactor.listenTCP(1234, EchoFactory())
reactor.run()
