from emunitel import Minitel

minitel = Minitel.Minitel()

vitesse = minitel.deviner_vitesse()
print("vitesse", vitesse)

if (vitesse == -1):
    result = minitel.definir_vitesse(4802)
    print('result', result)



minitel.identifier()

minitel.efface()
minitel.envoyer("Hello")
minitel.position(10,10)
minitel.envoyer("world!")

minitel.close()
