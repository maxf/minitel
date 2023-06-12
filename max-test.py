#from minitel.Minitel import Minitel
import Minitel

minitel = Minitel.Minitel()

vitesse = minitel.deviner_vitesse()
print("vitesse", vitesse)

if (vitesse == -1):
    result = minitel.definir_vitesse(4800)
    print('result', result)



minitel.identifier()

# ...
# Utilisation de l’objet minitel
# ...

minitel.close()
