import requests

SERVER_URL="http://localhost:5000"

class Minitel:

    def __init__(self):
        pass

    def deviner_vitesse(self) -> int:
        return 4801

    def definir_vitesse(self, vitesse: int) -> int:
        return vitesse

    def identifier(self):
        self.capacite = {
            'nom': 'Minitel inconnu',
            'retournable': False,
            'clavier': 'ABCD',
            'vitesse': 1200,
            'constructeur': 'Inconnu',
            '80colonnes': False,
            'caracteres': False,
            'version': None
        }

    def close(self):
        pass

    def envoyer(self, contenu):
        requests.post(
            SERVER_URL + '/envoyer',
            data={'contenu': contenu}
        )

    def recevoir(self, bloque = False, attente = None):
        requests.get(
            f'{SERVER_URL}/recevoir?bloque={bloque}&attente={attente}'
        )

    def position(self, colonne, ligne, relatif = False):
        requests.post(
            f'{SERVER_URL}/position',
            data={
                'colonne': colonne,
                'ligne': ligne,
                'relatif': relatif
            }
        )

    def efface(self, portee = 'tout'):
        requests.post(
            f'{SERVER_URL}/efface',
            data={
                'portee': portee
            }
        )

    def taille(self, largeur: int = 1, hauteur: int = 1):
        assert largeur in [1, 2]
        assert hauteur in [1, 2]
        requests.post(
            f'{SERVER_URL}/taille',
            data={
                'largeur': largeur,
                'hauteur': hauteur
            }
        )
