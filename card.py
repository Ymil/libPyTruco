'''

Autor: Lautaro Linquiman
Fecha: 04/08/16
Descripcion: Esta clase almacena la informacion de cada carta repartidas

'''

class Card:
    def __init__(self, cardStr, cardValue):
        self.cardStr = cardStr
        self.cardValue = cardValue

    def getText(self):
        return self.cardStr

    def getValue(self):
        return self.cardValue
