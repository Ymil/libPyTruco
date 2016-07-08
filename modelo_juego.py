import sqlite3 as lite

class modelo_juego():
    def __init__(self):
        self.con = lite.connect('.libPyTruco.db')
        self.conStable = False
        with self.con:
            self.conStable = True
            self.conCursor = self.con.cursor()
    def __createTables(self):
        if self.conStable:
            self.conCursor.execute('''CREATE TABLE mano
                (date text, trans text, symbol text, qty real, price real)''')
