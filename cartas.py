'''
Clase Cartas del juego
06-01-2015
Programador: Lautaro Linquiman
'''
from random import randrange
from card import Card
class Cartas():
    '''Clase encargada de el manejo de las cartas del juego'''
    def __init__(self,cantidadJugadores, debuggin = 1):
        self.debuggin = debuggin

        if(self.debuggin):
            print('Clase cartas iniciada')
        '''
        Puntaje de cada carta
        4 = 1
        5 = 2
        6 = 3
        7 Basto y Copa = 4
        10 = 5
        11 = 6
        12 = 7
        As Oro Y Copo = 8
        2 = 9
        3 = 10
        7 Oro = 11
        7 Espada = 12
        1 Basto = 13
        1 Espada = 14
        '''
        self.cantidadJugadores = cantidadJugadores
        self.cartas = ['oro_1','oro_2','oro_3','oro_4','oro_5','oro_6','oro_7','oro_10','oro_11','oro_12',
        'espada_1','espada_2','espada_3','espada_4','espada_5','espada_6','espada_7','espada_10','espada_11','espada_12',
        'basto_1','basto_2','basto_3','basto_4','basto_5','basto_6','basto_7','basto_10','basto_11','basto_12',
        'copa_1','copa_2','copa_3','copa_4','copa_5','copa_6','copa_7','copa_10','copa_11','copa_12']

        self.cartasPuntaje = {'oro_1':8,'oro_2':9,'oro_3':10,'oro_4':1,'oro_5':2,'oro_6':3,'oro_7':11,'oro_10':5,'oro_11':6,'oro_12':7,
        'espada_1':14,'espada_2':9,'espada_3':10,'espada_4':1,'espada_5':2,'espada_6':3,'espada_7':12,'espada_10':5,'espada_11':6,'espada_12':7,
        'basto_1':13,'basto_2':9,'basto_3':10,'basto_4':1,'basto_5':2,'basto_6':3,'basto_7':4,'basto_10':5,'basto_11':6,'basto_12':7,
        'copa_1':8,'copa_2':9,'copa_3':10,'copa_4':1,'copa_5':2,'copa_6':3,'copa_7':4,'copa_10':5,'copa_11':6,'copa_12':7}
        self.clonCartas = []
        self.cartasRepartidas = []

        self.cartasJugador = [] #Almacena las cartas de los jugadores

    def __clonarCartas(self):
        self.clonCartas = self.cartas[:]

    def prepararMaso(self):
        '''Esta funcion copia los valores y nombres de las cartas en una variable temporal.
         Esta funcion se debe llamar antes de repartir las cartas '''
        self.__clonarCartas()

    #def obtener(self, cartasN):

    def obtener(self, jugadorID, cartaID):
        return self.cartasJugadores[jugadorID-1][cartaID-1]

    def getPoints(self,cartaSTRID):
        return self.cartasPuntaje[cartaSTRID]

    def repartir(self):
        ''' Return list ((1,2,3),(1,2,3))'''

        self.__clonarCartas()

        #debuggin
        if(self.debuggin):
            print('Repartiendo carta')
        #debuggin

        cartasJugadores = [] #Cartas de los juegador repartidas
        for x in range(self.cantidadJugadores): #Recorre cada uno de los jugadores

            #debuggin
            if(self.debuggin):
                print(x)
            #debuggin

            cartasJugador = [] #Acomoda las cartas de cada jugador

            for c in range(3): #reparte las tres cartas a cada jugadores

                cartaStr = randrange(0,len(self.clonCartas) - 1)
                cartaValor = self.clonCartas[carta]
                cartaObject = Card(cartaStr,cartaValor)
                cartasJugador.append(cartaObject)
                self.clonCartas.remove(cartaStr)

            cartasJugadores.append(cartasJugador)

            cartasJugador = None

        #debuggin
        if(self.debuggin):
            print('Cartas Repartidas a jugar!')
            print(cartasJugadores)
        #debuggin

        self.cartasJugadores = cartasJugadores
        return cartasJugadores

    def repartir_individual(self):
        ''' Esta funcion reparte 3 cartas
        Return list (1,2,3)'''

        #debuggin
        if(self.debuggin):
            print('Repartiendo carta')

        #debuggin
        if(self.debuggin):
            print(x)
        #debuggin

        cartasJugador = [] #Acomoda las cartas de cada jugador

        for c in range(3): #reparte las tres cartas a cada jugadores
            cartaN = randrange(0,len(self.clonCartas) - 1)
            cartaStr = self.clonCartas[cartaN]
            cartaValue = self.cartasPuntaje[cartaStr]
            cartaObject = Card(cartaStr,cartaValue)
            cartasJugador.append(cartaObject)
            self.clonCartas.remove(cartaStr)
            del cartaObject


        #debuggin
        if(self.debuggin):
            print('Cartas Repartidas a jugar!')
            print(cartasJugador)
        #debuggin

        return cartasJugador
