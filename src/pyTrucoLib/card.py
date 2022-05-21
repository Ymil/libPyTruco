class Card:
    '''
    Descripcion: Esta clase almacena la informacion de cada carta repartidas
    '''

    def __init__(self, cardList):
        '''
        :param cardList: list[numTheCard, stick, value]
        '''
        self.cardList = cardList

    def __add__(self, otherCardObject):
        ''' Cuando se suman dos objectos de la clase Card se obtiene
        el puntaje total de las cartas para envido
        :param otherCardObject: CardObject
        :return: Devuelve la suma de puntos para el envido
        :rtype: int
        '''
        if self.getNumber() < 10:
            c1 = self.getNumber()
        else:
            c1 = 20

        if otherCardObject.getNumber() < 10:
            c2 = otherCardObject.getNumber()
        else:
            c2 = 20
        points = c1+c2
        if points < 20:
            points += 20
        elif points == 40:
            points -= 20
        return points

    def __str__(self):
        return self.getText()

    def getText(self):
        '''
        :return: Esta funcion devuelve el numero de la carta y el palo
        :rtype: str '''
        cardStr = '%d_%s' % (self.cardList[0], self.cardList[1])
        return cardStr

    def getNumber(self):
        '''
        :return: Esta funcion devuelve el numero de la carta
        :rtype: int '''

        return self.cardList[0]

    def getStick(self):
        '''
        :return: Esta funcion devuelve el palo de la carta
        :rtype: str'''
        return self.cardList[1]

    def getValue(self):
        ''':return: Esta funcion devuelve el valos de la carta
        :rtype: int'''
        return self.cardList[2]
