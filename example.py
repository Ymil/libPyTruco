'''
Simulacion de ejemplo de como utilizar la libreria PyTruco
@Autor: Lautaro Linquiman
@Email: acc.limayyo@gmail.com

Paso 1: Definir parametros de la Simulacion
    CantidadDeJugadores

Paso 2: Definir jugadores
Se importa el modulo jugador, el cual alamacena todos los parametros y funcionalidades.
'''
from jugador import Jugador

'''
Paso 3: Crear mesa
Se importa el modulo mesa, el cual alamacena todos los parametros y funcionalidades.
'''
from mesa import Mesa

''' Paso 5: Crear una nueva partida
Se importa el modulo Juego, el cual alamacena todos los parametros y funcionalidades.
'''
from juego import Juego


class EjemploDeTruco:
    def __init__(self):
        ''' Paso 1: Definiendo parametros de la simulacion '''
        self.cantidadDeJugadores = 2

        '''Paso 2: Definiendo jugadores'''
        self.jugadores = []
        self.jugadores.append(Jugador(0))
        self.jugadores.append(Jugador(1))

        ''' Paso : Creando mesa '''
        self.mesa = Mesa(self.cantidadDeJugadores, self.jugadores[0].getID(), 0)

        '''Paso 4: Asignando nuevos jugadores a la mesa'''
        self.mesa.newPlayer(self.jugadores[0])
        self.mesa.newPlayer(self.jugadores[1])

        #Se verifica que se pueda iniciar la partida
        if(self.mesa.getStatus()):
            ''' Paso 5: Creando una nueva partida '''
            equipos = self.mesa.getTeams() #Obtiene la configuracion de jugadores respecto a los equipos.
            self.juego = Juego(self.jugadores, equipos, self.mesa.getID())

            self.juego.iniciar()            


if __name__ == "__main__":
    EjemploDeTruco()
