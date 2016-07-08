'''
Controlador de Servidor 2 Jugadores
09-01-2015 Son las 3 y 04 de la manana
Lautaro Linquiman
'''


'''
CMDS
[msg] = Etiqueta de emision de mensajes
[get] = Obtener texto del cliente
'''

#debuggin
import sys
import traceback
#debuggin

from cmds import Cmds

class Controlador(Cmds):
	def __init__(self):
		''' 
		Estados de juego
		0 = Esperando jugadores
		1 = Mesa arma
		2 = Repartir cartas
		'''
		self.__estadoJuego = 0	
		
		self.manoJuego = 0 #Indica la mano del juego
		
		self.debuggin = 0
		self.idsJugadores = 1
		self.jugadoresIdentificados = 0
		self.jugadores = {}
	
	#Estados de juego
	def getStatus(self):
		return self.__estadoJuego
		
	def setStatus(self, estado):
		self.__estadoJuego = estado
	#Estados de juego
	
	#Mano del juego
	def getTurnoID(self):
		getIdsPlayers = self.getIDAllPlayers()
		return getIdsPlayers[self.manoJuego]
	
	def getSiguienteTurnoID(self):
		contrincanteID = self.manoJuego + 1
		if(contrincanteID == 2):
			self.manoJuego = 0
		getIdsPlayers = self.getIDAllPlayers()	
		return getIdsPlayers[contrincanteID]
	
	def cambioMano(self):
		self.manoJuego = self.manoJuego + 1
		if(self.manoJuego == 2):
			self.manoJuego = 0
			
	#Mano del juego
	
	def getIDAllPlayers(self):
		return self.jugadores.keys()
		
	def nuevaConexion(self,sc,addr):		
		self.jugadores[self.idsJugadores] = {'addr':(addr), 'sc':sc}
		self.idsJugadores = self.idsJugadores+1
		return self.idsJugadores-1
		
	def contarJugadores(self):
		if(self.jugadoresIdentificados == 2):
			return 1
		else:
			return 0
			
	def regNick(self, nombre, idJugador):
		if(self.debuggin == 1): print(self.jugadores[idJugador])
		if(idJugador):
			if(len(nombre) > 0):
				self.jugadores[idJugador]['nombre'] = nombre
				print("Nuevo jugador %s") % self.jugadores[idJugador]['nombre']
				self.jugadoresIdentificados = self.jugadoresIdentificados + 1
				return 1
			else:
				return 0
		else:
			return 0
		
	def getIdForName(self,nombre):
		''' Obtiene el id del jugador por su nombre '''
		for idJugador in range(self.idsJugadores):
			try:
				if(self.jugadores[idJugador]['nombre'] == nombre):
					return idJugador
			except Exception:
				continue
		return 0
	
	def getIdForAddres(self,addr):
		''' Obtiene el id del jugador por addres'''
		print(type(addr))
		for idJugador in range(self.idsJugadores):
			try:
				if(self.jugadores[idJugador]['addr'] == addr):
					return idJugador
			except Exception:
				traceback.print_exc(file=sys.stdout)
				print("Error GetIdForAddres")
				continue
		return 0

	
		
		
