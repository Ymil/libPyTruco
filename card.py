'''

Autor: Lautaro Linquiman
Fecha: 04/08/16
Descripcion: Esta clase almacena la informacion de cada carta repartidas

'''

class Card:
    def __init__(self, cardList):
        self.cardList = cardList

    def __add__(self, otherCard):
        ''' Cuando se suman dos objectos de la clase Card se obtiene
        el puntaje total de las cartas para envido '''
        c1 = self.getNumber() if self.getNumber() < 10 else 20
        c2 = otherCard.getNumber() if otherCard.getNumber() < 10 else 20
        points = c1+c2
        if points < 20:
            points += 20
        elif points == 40:
            points -= 20
        return points

    def getText(self):
        '''Esta funcion devuelve el numero de la carta y el palo

        @return str '''
        cardStr = '%d_%s' % (self.cardList[0], self.cardList[1])
        return cardStr

    def getNumber(self):
        '''Esta funcion devuelve el numero de la carta

        @return int '''

        return self.cardList[0]
        
    def getStick(self):
        '''Esta funcion devuelve el palo de la carta

        @return str'''
        return self.cardList[1]

    def getValue(self):
        '''Esta funcion devuelve el valos de la carta

        @return int'''
        return self.cardList[2]
