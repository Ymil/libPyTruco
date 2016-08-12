'''
Autor: Lautaro Linquiman
Fecha: 03/08/2016
Descripcion: Esta clase almacena la informacion del juego
'''


class Team:
    def __init__(self, ID):
        self.id = ID
        self.points = 0

    def getID(self):
        return self.id

    def givePoints(self, points):
        self.points += points

    def getPoints(self):
        return self.points
