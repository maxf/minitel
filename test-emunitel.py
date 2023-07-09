#from minitel import Minitel
from emunitel import Minitel
import time

NB_ROWS = 24
NB_COLS = 40

def test_screen():
    for row in range(1, NB_ROWS+1):
        for col in range(1, NB_COLS+1):
            minitel.position(col, row)
            minitel.envoyer('X')

minitel = Minitel.Minitel()

vitesse = minitel.deviner_vitesse()
print("vitesse", vitesse)

if (vitesse == -1):
    result = minitel.definir_vitesse(4802)
    print('result', result)

minitel.identifier()

minitel.efface()

#test_screen()


minitel.position(1, 2)
minitel.taille(2,2)
minitel.envoyer("1234567890")
minitel.envoyer("1234567890")
minitel.envoyer("1234567890")
minitel.envoyer("1234567890")
minitel.envoyer("1234567890")
minitel.taille(1,1)
minitel.envoyer("1234567890")
# minitel.taille(2,2)
# minitel.envoyer("12345")

# minitel.taille(1,1)
# minitel.envoyer("123456789")
# minitel.taille(2,2)
# minitel.envoyer("12345")
# minitel.taille(1,1)
# minitel.envoyer("1234567890")
# minitel.taille(2,2)
# minitel.envoyer("1234567")
# #minitel.envoyer("1234567890123456789012345678901234567890")



#minitel.position(6,6)
#minitel.envoyer("bleh!")

#minitel.taille(1,1)
#minitel.envoyer("yay!")

# minitel.position(18,2)
# minitel.taille(2,1)
# minitel.envoyer("yay!")

# minitel.position(26,2)
# minitel.taille(1,2)
# minitel.envoyer("cool!")

time.sleep(200)
minitel.close()
