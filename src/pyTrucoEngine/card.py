cards_dict = {
    # [Numero de carta, palo, valor]
    '1_oro': [1, 'oro', 8],
    '1_espada': [1, 'espada', 14],
    '1_basto': [1, 'basto', 13],
    '1_copa': [1, 'copa', 8],
    '2_oro': [2, 'oro', 9],
    '2_espada': [2, 'espada', 9],
    '2_basto': [2, 'basto', 9],
    '2_copa': [2, 'copa', 9],
    '3_oro': [3, 'oro', 10],
    '3_espada': [3, 'espada', 10],
    '3_basto': [3, 'basto', 10],
    '3_copa': [3, 'copa', 10],
    '4_oro': [4, 'oro', 1],
    '4_espada': [4, 'espada', 1],
    '4_basto': [4, 'basto', 1],
    '4_copa': [4, 'copa', 1],
    '5_oro': [5, 'oro', 2],
    '5_espada': [5, 'espada', 2],
    '5_basto': [5, 'basto', 2],
    '5_copa': [5, 'copa', 2],
    '6_oro': [6, 'oro', 3],
    '6_espada': [6, 'espada', 3],
    '6_basto': [6, 'basto', 3],
    '6_copa': [6, 'copa', 3],
    '7_oro': [7, 'oro', 11],
    '7_espada': [7, 'espada', 12],
    '7_basto': [7, 'basto', 4],
    '7_copa': [7, 'copa', 4],
    '10_oro': [10, 'oro', 5],
    '10_espada': [10, 'espada', 5],
    '10_basto': [10, 'basto', 5],
    '10_copa': [10, 'copa', 5],
    '11_oro': [11, 'oro', 6],
    '11_espada': [11, 'espada', 6],
    '11_basto': [11, 'basto', 6],
    '11_copa': [11, 'copa', 6],
    '12_oro': [12, 'oro', 7],
    '12_espada': [12, 'espada', 7],
    '12_basto': [12, 'basto', 7],
    '12_copa': [12, 'copa', 7],
}


class Card:
    """
    Descripcion: Esta clase almacena la informacion de cada carta repartidas
    """

    def __init__(self, card_name):
        """
        :param card_name: string type 1_basto
        :param cardList: list[numTheCard, stick, value]
        """
        self.cardList = cards_dict[card_name]

    def __add__(self, card) -> int:
        """ Cuando se suman dos objectos de la clase Card se obtiene
        el puntaje total de las cartas para envido
        :param otherCardObject: CardObject
        :return: Devuelve la suma de puntos para el envido
        :rtype: int
        """
        if self.getNumber() < 10:
            c1 = self.getNumber()
        else:
            c1 = 20

        if card.getNumber() < 10:
            c2 = card.getNumber()
        else:
            c2 = 20
        points = c1 + c2
        if points < 20:
            points += 20
        elif points == 40:
            points -= 20
        return points

    def __str__(self):
        return self.getText()

    def __repr__(self):
        return self.getText()

    def getText(self) -> str:
        """
        :return: Esta funcion devuelve el numero de la carta y el palo
        :rtype: str """
        return f'{self.cardList[0]}_{self.cardList[1]}'

    def getNumber(self) -> int:
        """
        :return: Esta funcion devuelve el numero de la carta
        :rtype: int """

        return self.cardList[0]

    def getStick(self) -> str:
        """
        :return: Esta funcion devuelve el palo de la carta
        :rtype: str"""
        return self.cardList[1]

    def getValue(self) -> int:
        """:return: Esta funcion devuelve el valos de la carta
        :rtype: int"""
        return self.cardList[2]
