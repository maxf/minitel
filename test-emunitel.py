from emunitel import Minitel
import time

minitel = Minitel.Minitel()

vitesse = minitel.deviner_vitesse()
print("vitesse", vitesse)

if (vitesse == -1):
    result = minitel.definir_vitesse(4802)
    print('result', result)

minitel.identifier()

minitel.efface()
minitel.position(1, 1)
minitel.envoyer("Hello")

minitel.position(10,10)
minitel.taille(2,2)
minitel.envoyer("world!")

minitel.position(15,4)
minitel.taille(2,1)
minitel.envoyer("yay!")

minitel.position(4,4)
minitel.taille(1,2)
minitel.envoyer("cool!")

time.sleep(200)
minitel.close()
