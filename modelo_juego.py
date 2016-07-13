import sqlite3 as lite
import json
class modelo_juego():
    def __init__(self):
        self.con = lite.connect('.juego.db')
        self.conStable = False
        with self.con:
            self.conStable = True
            self.conCursor = self.con.cursor()
            self.getInfoTable(1)

    def getInfoTable(self, id):
        self.conCursor.execute("select * from mesa where id = %d" % id)
        print type(self.conCursor),dir(self.conCursor)
        x = [row for row in self.conCursor][0]
        print x,type(x),x[0]
        print str(x[2])
        #rep = json.load(self.conCursor[2])
        #print rep
'''
python

from modelo_juego import modelo_juego as mj

jm = mj()

exit()

python


'''
