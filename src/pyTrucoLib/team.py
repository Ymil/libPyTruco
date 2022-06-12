#!/usr/bin/env python 2.7
__author__ = 'Lautaro Linquiman'
__email__ = 'acc.limayyo@gmail.com'
__status__ = 'Developing'


class Team:
    def __init__(self, ID):
        '''
        @author: Lautaro Linquiman
        03/08/2016
        Esta clase almacena la informacion del equipo
        :param ID: Numero identificador del equipo
        :rtype: objectTeam
        '''
        self.id = ID
        self.points = 0

    def getID(self):
        '''
        :return: Esta funcion devuelve el ID del equipo
        :rtype: int
        '''
        return self.id

    def givePoints(self, points):
        '''
        Esta funcion asigna puntos al equipo
        :param points: int
        '''
        self.points += points

    def getPoints(self):
        '''
        :return: Esta funcion devuelve los puntos del equipo
        :rtype: int
        '''
        return self.points

    def __str__(self):
        return f'Team: {self.id} Points: {self.points}'
