from emunitel import Minitel
import time

minitel = Minitel.Minitel()

minitel.efface()
time.sleep(4)
minitel.position(0, 0)
minitel.envoyer("Hello")
time.sleep(4)
minitel.position(10,10)
minitel.taille(2,1)
minitel.envoyer("world!")

minitel.close()
