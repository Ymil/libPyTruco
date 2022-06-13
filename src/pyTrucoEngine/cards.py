from random import randrange
from typing import List

from .card import Card
from .card import cards_dict


class Cards():
    '''Clase encargada de el manejo de las cartas del juego'''

    def __init__(self):
        self.clon_cards = []
        self.cartasRepartidas = []

    def __clonarCartas(self):
        self.clon_cards = cards_dict.keys()

    def prepararMaso(self) -> None:
        '''Esta funcion copia los valores y nombres de las
         cartas en una variable temporal.
         Esta funcion se debe llamar antes de repartir las cartas '''
        self.__clonarCartas()

    def repartir_individual(self) -> List[Card]:
        ''' Esta funcion reparte 3 cartas
        Return list (1,2,3)'''

        cards = []  # Acomoda las cartas de cada jugador
        for _ in range(3):  # reparte tres cartas aleatorias
            cartaN = randrange(0, len(self.clon_cards) - 1)
            card_name = self.clon_cards[cartaN]
            card = Card(card_name)
            cards.append(card)
            del self.clon_cards[cartaN]
            del card

        return cards
