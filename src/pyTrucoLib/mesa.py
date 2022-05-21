#!/usr/bin/env python 2.7
__author__ = "Lautaro Linquiman"
__email__ = "acc.limayyo@gmail.com"
__status__ = "Developing"

from .handlers.signals import signals
from .team import Team


class Mesa:
    def __init__(self, signalsHandler: signals, cantidadJugadores, creadaPor, mesaID):
        """
        Esta clase contiene toda la funcionalidad para crear y
        manejar las mesas
        2015-01
        @author: Lautaro Linquiman
        :param cantidadJugadores: int
        :param creadaPor: int idJugador
        :param mesaID: int ID de la mesa
        """
        self.cantidadJugadores = cantidadJugadores
        self.creadaPor = creadaPor
        self.mesaID = mesaID
        self.jugadores = []
        self.equipoJugadores = []
        self.equipoN = 0
        self.status = 0
        self.team = []  # Almacena los objectos de los equipos
        self.signals_handler: signals = signalsHandler
        self.__createTeams__()

    def getInfo(self):
        """ Retorna informacion sobre la mesa
        :return: (mesaID, cantidadJugadores, cantidadJugadores, creadaPor)
        :rtype: tuple
        """
        return (
            self.mesaID,
            self.cantidadJugadores,
            len(self.jugadores),
            self.creadaPor,
        )

    def getStatus(self):
        """
        :return: true si la cantidad de jugadores en la mesa es
        igual a la que se indico
        :rtype: bool
        """
        print(len(self.jugadores))
        if self.cantidadJugadores == len(self.jugadores):
            self.status = 1
            return True
        else:
            self.status = 0
            return False

    def __createTeams__(self):
        self.team.append(Team(1))
        self.team.append(Team(2))

    def newPlayer(self, playerObject):
        """
        Ingresa un nuevo jugador a la mesa
        :param playerObject:"""
        self.jugadores.append(playerObject)
        playerObject.setTeam(self.team[self.equipoN])
        self.equipoN += 1
        if self.equipoN == 2:
            self.equipoN = 0

    def getPlayers(self):
        """
        :return: Devuelve todos los jugadores
        :rtype: list"""
        return self.jugadores

    def getTeams(self):
        """
        :return: Equipos
        :rtype: list"""
        return self.team

    def getID(self):
        """
        :return: ID de la mesa
        :rtype: int"""
        return self.mesaID
