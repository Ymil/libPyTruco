from typing import List

from .player import Player


class Team:
    def __init__(self, ID: int):
        '''
        @author: Lautaro Linquiman
        03/08/2016
        Esta clase almacena la informacion del equipo
        :param ID: Numero identificador del equipo
        :rtype: objectTeam
        '''
        self.id: int = ID
        self.players: List[Player] = []
        self.points = 0

    def add_player(self, player) -> None:
        self.players.append(player)

    def getID(self) -> int:
        '''
        :return: Esta funcion devuelve el ID del equipo
        :rtype: int
        '''
        return self.id

    def givePoints(self, points: int) -> None:
        '''
        Esta funcion asigna puntos al equipo
        :param points: int
        '''
        self.points += points

    def getPoints(self) -> int:
        '''
        :return: Esta funcion devuelve los puntos del equipo
        :rtype: int
        '''
        return self.points

    def get_envido_points(self) -> int:
        """
        :return: Devuelve el maximo numero de puntos para el envido de los
            jugadores del equipo.
        :rtype: int
        """
        return max(
            list(map(lambda player: player.getPointsEnvido(), self.players)),
        )

    def __str__(self):
        return f'Team: {self.id} Points: {self.points}'
