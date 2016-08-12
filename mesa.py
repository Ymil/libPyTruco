''' Paso x: Crear equipos
Se importa el modulo equipo el cual almacena la informacion de cada equipo
'''

from team import Team

class Mesa():
    def __init__(self, cantidadJugadores, creadaPor, mesaID):
        '''
        Esta clase crea una mesa de partida
        @cantidadJugadores int
        @creadoPor int idJugador
        @mesaID int ID de la mesa
        '''
        self.cantidadJugadores = cantidadJugadores
        self.creadaPor = creadaPor
        self.mesaID = mesaID
        self.jugadores = []
        self.equipoJugadores = []
        self.equipoN = 0
        self.status = 0
        self.team = [] #Almacena los objectos de los equipos
        self.__createTeams__()

    def getInfo(self):
        ''' Retorna informacion sobre la mesa '''
        return (self.mesaID, self.cantidadJugadores, len(self.jugadores), self.creadaPor)

    def getStatus(self):
        ''' Devuelve true si la cantidad de jugadores en la mesa es igual a la que se indico'''
        print(len(self.jugadores))
        if(self.cantidadJugadores == len(self.jugadores)):
            self.status = 1
            return 1
        else:
            self.status = 0
            return 0
    def __createTeams__(self):
        self.team.append(Team(1))
        self.team.append(Team(2))

    def newPlayer(self, player):

        ''' @params
        class player
        Ingresa un nuevo jugador a la mesa'''
        self.jugadores.append(player)
        player.setTeam(self.team[self.equipoN])
        self.equipoN += 1
        if(self.equipoN == 2):
            self.equipoN = 0

    def getPlayers(self):
        ''' Obitne las id de los jugadores '''
        return self.jugadores

    def getTeams(self):
        '''Retorna la configuracion de equipos '''
        return self.team

    def getID(self):
        '''Retorna el ID de la mesa'''
        return self.mesaID
