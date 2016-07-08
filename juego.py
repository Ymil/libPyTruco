from cartas import Cartas
from accionesJuego import AccionesJuego
import logging
logging.basicConfig(format='%(levelname)s [%(asctime)s][SVR]: %(message)s',filename='./logs/libjuego.log', level='DEBUG')
import inspect
import time
global cuentaEjecucion
cuentaEjecucion = 0
import string
def msg_debug(str1):
    global cuentaEjecucion
    #if(type(str1) is list):
    #    str1 = ' | '.join(tuple(list(str1))[0:])
    #print cuentaEjecucion
    str1 = 'EC %d' % cuentaEjecucion, str1
    #str1 = string.join(, ' ')
    logging.debug(str1)
    cuentaEjecucion += 1
class Juego():
    ''' Clase controlador del Juego
    20-01-15 05:07 Lautaro Linquiman'''
    def __init__(self, jugadores, jEquipos, mesaID):
        self.status = 0
        self.jugadores = jugadores
        self.jEquipos = jEquipos
        self.cantidadJugadores = len(jugadores) #Obtiene la cantidad de jugadores
        self.cartasJugador = []
        self.cartasJugadas = {}
        self.puntosEquipos = {1:0,2:0}
        self.equipoGanadorPrimeraRonda = 0
        self.equipoGanadorSegundaRonda = 0
        #self.primerJugadorPartida = 0
        self.mesaID = mesaID
        self.pardaObtenerGanador = 0
        self.ronda = 0
        self.rondas = {}
        self.mano = 0
        self.turno = 0
        self.cartas_ = Cartas(self.cantidadJugadores, 0)
        self.actionGame = AccionesJuego()
        self.returnObtenerGanador = {
            'status':0,
            'playerid': 0,
            'playeridWin': 0,
            'playerTeam': 0,
            'teamWin': 0,
            'roundWin': 0,
            'card': '', #str Type
            'cardWin': 0,
        }
        self.returnObtenerGanador = self.returnObtenerGanador
    def setActionGame(self, classActionGame):
        self.actionGame = classActionGame()

    def getStatus(self):
        return self.status

    def setStatus(self,status):
        self.status = status

    def getTurno(self):
        ''' Obtiene el id del jugador que es mano '''
        msg_debug('[getTurno-turno] %d' % self.turno)
        if(self.turno == self.cantidadJugadores):
            self.turno = 0
        turno = self.jugadores[self.turno]
        self.cambiarTurno()
        return turno

    def cambiarTurno(self):
        ''' Cambia la mano del juego '''
        if(self.turno == self.cantidadJugadores):
            self.turno = 0
        else:
            self.turno += 1

    def setTurno(self, jugadorID):
        self.turno = self.jugadores[jugadorID].getID()
        if(self.turno == self.cantidadJugadores):
            self.turno = 0
        self.turno = self.turno

    def decCartaID(self, carta):
        ''' Valida que el valor ingresado por el jugador sea valido '''
        try:
            cartaID = int(carta)
            if(cartaID <= 3):
                return cartaID-1
            else:
                return 20
        except ValueError:
            return 20

    def iniciarRonda(self):
        ''' Inicia la ronda '''
        self.ronda += 1
        self.rondas[self.ronda] = []
        self.mano = self.getTurno()
        return self.ronda

    def resetRonda(self):
        self.ronda = 0
        self.pardaObtenerGanador = 0
    def getRonda(self):
        return self.ronda

    def repartirCartas(self):
        ''' Reparte la carta de los jugaodres '''
        self.cartasJugador = self.cartas_.repartir()
        return self.cartasJugador

    def darCartas(self, nJugador):
        self.cartasJugadas[nJugador] = []
        return self.cartasJugador[nJugador]

    def setCarta(self, jugadorID, cartaID):
        nRonda = self.getRonda()
        self.rondas[nRonda].append((jugadorID, cartaID))

    def darPuntosEquipo(self, equipo, puntos):
        self.puntosEquipos[equipo] += puntos

    def getPuntosEquipos(self):
        return self.puntosEquipos

    def obtenerGanador(self):
        '''
        Esta funcion busca un ganador de la mano jugada y devuelve el estado que termino la mano
        @params
        null

        @return
        {
            'status': int [0:win|1:parda|2:empate|3:continue],
            'playerid': [idJugadorGanador],
            'teamWin': [idEquipoGanador]
            'cardWin': [CartaGandora],
            'roundWin': int Se gano la ronda [0|1]
        }
        '''

        nRonda = self.getRonda()

        '''
        cartaMayor[0] Indica la carta ganadora
        returnObtenerGanador['playerid'] Indica el IDjugador ganador
        '''

        parda = 0
        msg_debug('Ejecutando %s' % inspect.stack()[0][3])
        str1 = 'Rondas ', len(self.rondas),'/', self.rondas
        msg_debug(str1)
        self.returnObtenerGanador['cardWin'] = 0
        for ronda in self.rondas[nRonda]:
            #print dir(ronda)

            self.returnObtenerGanador['playerid'] = ronda[0]
            self.returnObtenerGanador['playerTeam'] = self.jEquipos[self.returnObtenerGanador['playerid']]
            self.returnObtenerGanador['card'] = ronda[1]

            msg_debug('[obtenerGanador-cartaSTR] %s' % self.returnObtenerGanador['card'])
            puntajeCartaJugador = self.cartas_.getPoints(self.returnObtenerGanador['card'])
            if(nRonda == 1):
                ''' Se setean la variables para iniciar el juego '''
                self.equipoGanadorPrimeraRonda = 0
                self.equipoGanadorSegundaRonda = 0
                self.pardaObtenerGanador = 0

            if(self.returnObtenerGanador['cardWin'] == 0):
                msg_debug("[Carta Ganadora] Todavia no hay una carta ganadora")
                puntajeCartaMayor = 0
            else:
                puntajeCartaMayor = self.cartas_.getPoints(self.returnObtenerGanador['cardWin'])
                msg_debug("[Carta Ganadora] %s:%d" % (self.returnObtenerGanador['cardWin'], puntajeCartaMayor))
            if(puntajeCartaJugador > puntajeCartaMayor):
                self.returnObtenerGanador['playeridWin'] = self.returnObtenerGanador['playerid']
                self.returnObtenerGanador['teamWin'] = self.returnObtenerGanador['playerTeam']
                self.returnObtenerGanador['cardWin'] = self.returnObtenerGanador['card']
                parda = 0
            elif(puntajeCartaJugador == puntajeCartaMayor):
                self.returnObtenerGanador['cardWin'] = self.returnObtenerGanador['card']
                parda = 1
        print(self.returnObtenerGanador['teamWin'])
        equipoWinManoActual = self.returnObtenerGanador['teamWin']
        msg_debug("Parda %d" % parda)
        if(self.ronda == 1):
            if(parda == 1):
                self.pardaObtenerGanador = 1
                self.parda()
            print 'oh'
            self.equipoGanadorPrimeraRonda = equipoWinManoActual
            self.setTurno(self.returnObtenerGanador['playeridWin'])
            self.continuarRonda()
        elif(self.ronda == 2):
            if(self.pardaObtenerGanador == 1 or parda == 1):
                if(parda == 0):
                    self.ganadorDeRonda()
                elif((parda == 0 and self.pardaObtenerGanador == 1) or (parda == 1 and self.pardaObtenerGanador == 0)):
                    self.returnObtenerGanador['teamWin'] = self.equipoGanadorSegundaRonda
                    self.ganadorDeRonda()
                elif(parda == 1 and self.pardaObtenerGanador == 1):
                    self.parda()

            self.equipoGanadorSegundaRonda = equipoWinManoActual
            if(equipoWinManoActual == self.equipoGanadorPrimeraRonda):
                self.ganadorDeRonda()
            else:
                self.continuarRonda()
                self.setTurno(self.returnObtenerGanador['playerid'])

        elif(self.ronda == 3):
            if(self.pardaObtenerGanador == 1 or parda == 1):
                if(parda == 0):
                    self.ganadorDeRonda()
                elif(parda == 1):
                    self.empate()
            msg_debug("Equipo Ganador Mano Actual: %s" % equipoWinManoActual)
            msg_debug("Equipo Ganador Mano 2: %s" % self.equipoGanadorSegundaRonda)
            msg_debug("Equipo Ganador Mano 1: %s" % self.equipoGanadorPrimeraRonda)
            if(equipoWinManoActual == self.equipoGanadorPrimeraRonda):
                self.ganadorDeRonda()
            elif(equipoWinManoActual == self.equipoGanadorSegundaRonda):
                self.returnObtenerGanador['teamWin'] = self.equipoGanadorSegundaRonda
                self.ganadorDeRonda()
            msg_debug(self.returnObtenerGanador)
        return self.returnObtenerGanador

    def empate(self):
        self.returnObtenerGanador['status'] = 2
        self.returnObtenerGanador['roundWin'] = 1
        self.returnObtenerGanador['teamWin'] = self.mano

    def ganadorDeRonda(self):
        self.returnObtenerGanador['status'] = 0
        self.returnObtenerGanador['roundWin'] = 1

    def parda(self):
        self.returnObtenerGanador['status'] = 1

    def continuarRonda(self):
        self.returnObtenerGanador['status'] = 3

    def iniciar(self):
        msg_debug("Iniciando Juego")
        self.actionGame.setTeams(self.jEquipos)
        self.actionGame.setPlayers(self.jugadores)
        while 1:
            for equipo in self.getPuntosEquipos():
                self.actionGame.showPoints(equipo, self.puntosEquipos[equipo])
                #print ('puntos equipo %d: %d') %(equipo, self.puntosEquipos[equipo])
            ''' Repartir cartas '''
            cartasJugadores = self.repartirCartas()
            cx = 0
            for jugador in self.jugadores:
                cartas = cartasJugadores[cx]
                self.actionGame.giveCards(jugador.getID(), cartas);
                jugador.setCards(cartas)
                self.actionGame.showCards(jugador.getID(), cartas)
                cx += 1

            while 1:
                nRonda = self.iniciarRonda()
                ''' Se inicia el juego con el jugador que es mano '''
                cJugadas = 0 #Alamacena la cantidad de jugadas en la ronda
                while cJugadas < self.cantidadJugadores:
                    '''Se inicia el juego'''
                    cJugadas += 1
                    jugador = self.getTurno()

                    while 1:
                        cartaAJugar = self.actionGame.getActionPlayer(jugador.getID())
                        carta = self.decCartaID(cartaAJugar) #Corrobora que el valor de la carta sea correcto
                        if(not carta == 20):
                            if(jugador.playingCard(carta)): #Juega la carta y se comprueba que este disponible
                                cartaJ = jugador.getCardPlayed() #Obitene el nombre completo de la carta
                                self.setCarta(jugador.getID(),cartaJ)
                                self.actionGame.showJugada(jugador.getTeam(), jugador.getID(), jugador.getName(),cartaJ)
                                break
                            else:
                                self.actionGame.showError(jugador.getID(), 'cardPlayerd')
                        else:
                            self.actionGame.showError(jugador.getID(), 'invalidAction')
                Resultados = self.obtenerGanador()
                self.actionGame.returnStatus(Resultados)
                print Resultados

                if(Resultados['status'] == 1):
                    self.actionGame.Parda()
                    continue

                self.actionGame.showResultMano(Resultados['playeridWin'], self.jugadores[Resultados['playeridWin']].getName(),  Resultados['playerTeam'],  Resultados['cardWin'])
                if(Resultados['roundWin']):
                    if(Resultados['status'] == 0):
                        self.actionGame.win(Resultados['teamWin'])
                    elif(Resultados['status'] == 2):
                        self.actionGame.winEmpate(Resultados['teamWin'])
                    self.darPuntosEquipo(Resultados['teamWin'],2)
                    self.resetRonda()
                    break

            break
        msg_debug("Juego Terminado")
