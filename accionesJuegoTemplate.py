#!/usr/bin/env python 2.7\n# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
__author__ = "Lautaro Linquiman"
__email__ = "acc.limayyo@gmail.com"
__status__ = "Developing"
__date__ = " 04/08/16"
import logging
import pdb
logging.basicConfig(format='[AccionesJuego] %(levelname)s [%(asctime)s]: %(message)s',filename='/home/ymil/Proyectos/PyTrucoProyect/PyTruco/servidor/libPyTruco/logs/accionGame.log', level='DEBUG')
import random

class AccionesJuegoTemplate:
    '''
    Esta clase almacena los eventos que se disparan a medida que se va ejecuntado el juego.

    Como mostrar mensajes, dar cartas etc.

    Esta clase es de ejemplo
    '''
    def __init__(self):
        self.players = []
        self.teams = []
        self.errors = {'cardPlayerd': 'Esta carta ya fue jugada', 'invalidAction': 'No puedes realizar esta accion'}

    def showMsgStartGame(self, players):
        ''' Esta funcion se dispara cuando se inicia un nuevo juego
        @param players:
        '''
        logging.debug("startGame")

    def showMsgStartRound(self):
        ''' Esta funcion se dispara cuando se inicia una nueva ronda
        '''
        logging.debug("startRound")

    def showMsgStartHand(self, handsNumber):
        ''' Esta funcion se llama cada vez que se inicia una nueva mano
        @param handsNumber: int'''
        str1 =  ("Iniciando mano %d" % handsNumber).center(50,'-')
        print str1
        logging.debug("startHand(%d)" % handsNumber)
        logging.info(str1)

    def showMsgFinishHand(self):
        ''' Esta funcion se dispara cuando finaliza una mano
        '''
        logging.debug("finishHand")

    def showMsgFinishRound(self):
        ''' Esta funcion se dispara cuando finaliza una ronda
        '''
        logging.debug("finishRound")

    def showMsgFinishGame(self):
        ''' Esta funcion se dispara cuando finaliza un juego
        '''
        logging.debug("finishGame")


    def giveCards(self, playerid, cards):
        ''' Esta funcion se dispara cuando se reparten las cartas,
        recibe como parametro el playerid y las cartas del jugador
        @param playerid:
        @param cards: list cardsObjects
        Ejemplo de uso:
        partida.mostrarCartas(player, cards) '''

        pass
    def showCards(self, playerid, cards):
        ''' Esta funcion se dispara cuando se le muestran las cartas al jugador
        params
        @param playerid:
        @param cards: list cardsObjects
        '''


    def showPoints(self, team, pointsTeam):
        ''' Esta funcion se dispara cuando se muestran los puntos de los equipos
        @param team: int teamID
        @param pointsTeam: int
        Ejemplo de uso: '''

        str1 = "El equipo %d tiene %d puntos" % (team, pointsTeam)
        print str1
        str2 = "teamPoints(%d,%d)" % (team, pointsTeam)
        logging.debug(str2)
        logging.info(str1)

    def getActionPlayer(self, playerObject, gameInfo = {}, quiero = False):
        ''' Esta funcion se llama cuando se tiene que obtener un accion del jugador


        @param playerObject:
        @param gameInfo: contiene información del juego

        @return:Esta funcion entrega informacion del estado juego en la variable infoGame
        @rtype: list


        Ejemplo:
        accion = raw_input("Escriba la accion o carta a jugar>")
        return accion(accion, valorAccion)

        Acciones[JugadorCarta, envido, real envido, falta envido, truco, re truco, vale 4]

        formato de respuesta: (accion, valor)
        '''

        ''' Las siguientes funciones generan jugadas de forma aleatoria para debuggiar el sistema. '''
        accionRDM = random.randint(0,10) #Obtiene un numero aleatorio para determinar una accion
        #pdb.set_trace()
        accion = []
        quiero = False if len(gameInfo['envido']) == 0 or 'winner' in gameInfo['envido'] else True
        if quiero == True:
            accion.append('Quiero')
            accion.append(random.randint(0,1))
        elif gameInfo['hand'] == 0 and accionRDM%2 == 0 and len(gameInfo['envido']) == 0:
            ''' La condicion len(gameInfo['envido']) == 0 significa que todavia no se canto el envido '''

            accion.append('envido')
        else:
            accion.append('JugarCarta')
            accion.append(random.randint(0,2))
        str1 = "getActionPlayer %d" % playerObject.getID(),accion
        logging.debug(str1)
        return accion

    def showCardPlaying(self, teamObject, playerObject, cardObject):
        ''' Esta funcion se llama cuando se juega una carta
        @param teamObject:
        @param playerObject:
        @param cardObject:
        Ejemplo:
        '''
        str1 = 'El jugador %d:%d jugo la carta %s' % (teamObject.getID(), playerObject.getID(), cardObject.getText())
        print str1
        logging.info(str1)
        str2 = 'showCardPlaying(%d,%d,%s)' % (teamObject.getID(), playerObject.getID(), cardObject.getText())
        logging.debug(str2)

    def showError(self, playerObject, errorName):
        ''' Esta funcion se llama cuando ocurre un error por un jugador
        @param playerObject:
        @param errorName: str ['cardPlayerd', 'invalidAction']
        Ejemplo:
        '''
        #print self.errors[errorName]
        pass

    def showResultaTheHand(self, playerid, playername, teamid, cardObject):
        ''' Esta funcion se llama cuando termina una mano

        @param playerid: int
        @param playername: str Nombre del jugador
        @param teamid: int
        @param cardObject:
        Ejemplo:'''
        str1 =  '%d:%d gano la mano con %s' % (teamid, playerid, cardObject.getText())
        print str1
        logging.info(str1)
        str2 = 'showResultaTheHand(%d,%d,%s)' % (teamid, playerid, cardObject.getText())
        logging.debug(str2)


    def Parda(self):
        ''' Esta funcion se llama cuando termina la mano y hay una parda

        none'''
        str1 = 'Ocurrio una parda'
        logging.info(str1)
        logging.debug("parda")

    def returnStatus(self, statusGame):
        ''' Esta funcion se llama cada vez que se busca un ganador
        @param statusGame: [StatusGame=(win,empate), teamWinner], [StatusGame=empate, CartaMayor], [StatusGame=continue, CartaMayor, playerid]
        '''
        #logging.debug("ReturnStatus")
        #print 'Status:',statusGame
        pass

    ''' Win Actions '''
    def winEmpate(self, teamIDWinner):
        ''' Esta funcion se llama cuando ocurre un empate

        @param teamIDWinner: int
        '''
        str1 = 'Ocurrio un empate, los puntos son para el equipo %d' % teamIDWinner
        print str1
        logging.info(str1)

    def win(self, teamIDWinner):
        ''' Esta funcion se llama cuando se gana la ronda

        @param teamIDWinner: int
        '''
        str1 = 'El equipo %s gano la ronda' % teamIDWinner
        print str1
        logging.info(str1)

    def winGameTeam(self, teamObject):
        ''' Esta funcion se llama cuando un equipo gana el juego

        @param teamObject:
        '''
        str1 = 'El equipo %d gano el juego' % teamObject.getID()
        print str1
        logging.info(str1)

    ''' Start Quiero/Noquiero '''

    def quiero(self, playerObject):
        ''' Esta funcion se llama cuando un jugador quiere a un canto

        @param playerObject:
        '''

        str1 = 'El jugador %d dijo quiero' % playerObject.getID()
        str2 = 'Quiero(%d)' % playerObject.getID()
        print str1
        logging.info(str1)
        logging.debug(str2)

    def noQuiero(self, playerObject):
        ''' Esta funcion se llama cuando un jugador no quiere a un canto

        @param playerObject:
        '''

        str1 = 'El jugador %d dijo no quiero' % playerObject.getID()
        str2 = 'noQuiero(%d)' % playerObject.getID()
        print str1
        logging.info(str1)
        logging.debug(str2)

    ''' Finish Quiero/Noquiero '''

    ''' startEnvidoBlock '''

    def startLoopEnvido(self):
        ''' Esta funcion se llama cuando se inicia el loop del envido '''
        logging.debug("startLoopEnvido")

    def finishLoopEnvido(self):
        ''' Esta funcion se llama cuando finaliza el loop del envido '''
        logging.debug("finishLoopEnvido")

    def envido(self, playerObject):
        '''
        Esta funcion se llama cuando alguien canta envido
        @param playerObject:
        '''
        str1 = 'El jugador %d canto envido' % playerObject.getID()
        str2 = 'envido(%d)' % playerObject.getID()
        print str1
        logging.info(str1)
        logging.debug(str2)

    def showEnvido(self, playerObject):
        '''
        Esta funcion se llama cuando un jugar canta su envido
        @param playerObject: '''
        str1 = 'El jugador %d tiene %d de envido' % (playerObject.getID(),playerObject.getPointsEnvido())
        str2 = 'showEnvido(%d,%d)' % (playerObject.getID(),playerObject.getPointsEnvido())
        print str1
        logging.info(str1)
        logging.debug(str2)

    def showWinnerEnvido(self,playerObject):
        '''
        Esta funcion se llama cuando se define un ganador del envido
        @param playerObject:
        '''

        str1 = 'El jugador %d gano el envido' % playerObject.getID()
        str2 = 'winnerEnvido(%d)' % playerObject.getID()
        print str1
        logging.info(str1)
        logging.debug(str2)
    ''' endEnvidoBlock '''

    def setPlayers(self,playerObject):
        pass
