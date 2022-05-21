import json
import threading
import time

from twisted.internet import protocol
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import WebSocketServerFactory
from pyTrucoLib.handlers.signals import signals
from pyTrucoLib.juego import Game
from pyTrucoLib.jugador import Jugador
from pyTrucoLib.table import Table
from pyTrucoLib.card import Card
from jsonSignalAdapter import json_signal_adapter

class web_socket_signals_adapter(json_signal_adapter):
    def sendMessageAll(self, msg):
        for player in self.players:
            player.sendMessage(str.encode(f"{msg}"))

    def sendMessageToPlayer(self, player, msg):
        player.sendMessage(str.encode(f"{msg}"))


class GameManager(web_socket_signals_adapter):
    id: int = 0

    def startGame(self):
        mesa = Table(2, 1, 0)
        for player in self.players[-2:]:
            mesa.newPlayer(player)
            player.sendMessage(
                str.encode(
                    json.dumps(
                        {
                            "action": "config_player",
                            "payload": {
                                "playerid": player.getID(),
                                "teamid": player.team.getID(),
                            },
                        }
                    )
                )
            )
        juego = Game(mesa, self)
        juego.start()

    def newPlayer(self, player):
        self.players.append(player)
        return len(self.players)

    def checkStartGame(self):
        if len(self.players) % 2 == 0:
            # Comenzamos el juego
            threading.Thread(target=self.startGame).start()


gameManager = GameManager()


class MyServerProtocol(WebSocketServerProtocol, Jugador):
    def onOpen(self):
        player_id = gameManager.newPlayer(self)
        Jugador.__init__(self, player_id)
        gameManager.checkStartGame()
        self.sendMessage(
            str.encode(
                json.dumps(
                    {"action": "msg", "payload": "Bienvenido al PyTruco Argentino"}
                )
            )
        )
        return super().onOpen()

    def onMessage(self, payload, isBinary):
        self.waitData = payload

    def awaitForResponse(self, player):
        self.waitData = ""
        self.sendMessage(
            str.encode(json.dumps({"action": "getAction", "payload": None,}))
        )
        while 1:
            if len(self.waitData) > 0:
                return self.waitData.decode()
            time.sleep(0.5)


if __name__ == "__main__":

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory()
    factory.protocol = MyServerProtocol
    reactor.listenTCP(9000, factory)
    reactor.run()

