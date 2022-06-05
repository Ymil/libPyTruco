import json
import threading
import time

from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from jsonSignalAdapter import json_signal_adapter
from pyTrucoLib.card import Card
from pyTrucoLib.controllers.game_controller import game_controller
from pyTrucoLib.handlers.signals import signals
from pyTrucoLib.player import Player
from pyTrucoLib.table import Table
from twisted.internet import protocol


class web_socket_signals_adapter(json_signal_adapter):
    def sendMessageAll(self, msg):
        for player in self.players:
            player.sendMessage(str.encode(f'{msg}'))

    def sendMessageToPlayer(self, player, msg):
        player.sendMessage(str.encode(f'{msg}'))


class GameManager():
    id: int = 0
    players: list = []
    tables: list[Table] = []

    def getTables(self, player):
        r_ = []
        for idx, table in enumerate(self.tables):
            r_.append([idx, table.getInfo()[1], idx])

        player.sendMessage(
            str.encode(
                json.dumps({'action': 'refresh_tables', 'payload': r_}),
            ),
        )

    def createTable(self, player):
        self.tables.append(
            Table(2, 1, 0),
        )

        player.sendMessage(
            str.encode(
                json.dumps({
                    'action': 'join_to_table',
                    'payload': len(self.tables) - 1,
                }),
            ),
        )

    def joinPlayerToTable(self, player, tableID):
        table = self.tables[int(tableID)]
        if(not table.getStatus()):
            table.newPlayer(player)
            if(table.getStatus()):
                for player in table.getPlayers():
                    player._conState = 2
                    player.sendMessage(
                        str.encode(
                            json.dumps(
                                {
                                    'action': 'config_player',
                                    'payload': {
                                        'playerid': player.getID(),
                                        'teamid': player.team.getID(),
                                    },
                                },
                            ),
                        ),
                    )
                juego = game_controller(
                    set(table.getTeams()), table.getPlayers(
                    ), web_socket_signals_adapter(table.getPlayers()),
                )
                threading.Thread(target=juego.start).start()

    def newPlayer(self, player):
        self.players.append(player)
        return len(self.players)


gameManager = GameManager()


class playerCon(WebSocketServerProtocol, Player):
    _conState = 1

    def onOpen(self):
        player_id = gameManager.newPlayer(self)
        Player.__init__(self, player_id)
        self.sendMessage(
            str.encode(
                json.dumps(
                    {'action': 'msg', 'payload': 'Bienvenido al PyTruco Argentino'},
                ),
            ),
        )
        return super().onOpen()

    def onMessage(self, payload, isBinary):
        payload = payload.decode()
        if self._conState == 1:
            spayload = payload.split(',')
            if spayload[0] == 'get_tables':
                gameManager.getTables(self)
            elif spayload[0] == 'create_table':
                gameManager.createTable(self)
            elif spayload[0] == 'join':
                gameManager.joinPlayerToTable(self, spayload[1])
            return
        self.waitData = payload

    def awaitForResponse(self, player):
        self.waitData = ''
        self.sendMessage(
            str.encode(json.dumps({'action': 'getAction', 'payload': None})),
        )
        while 1:
            if len(self.waitData) > 0:
                return self.waitData
            time.sleep(0.5)


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory()
    factory.protocol = playerCon
    reactor.listenTCP(9000, factory)
    reactor.run()
