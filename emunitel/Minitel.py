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
        """Définit la taille des prochains caractères

        Le Minitel est capable d’agrandir les caractères. Quatres tailles sont
        disponibles :

        - largeur = 1, hauteur = 1: taille normale
        - largeur = 2, hauteur = 1: caractères deux fois plus larges
        - largeur = 1, hauteur = 2: caractères deux fois plus hauts
        - largeur = 2, hauteur = 2: caractères deux fois plus hauts et larges

        Note:
        Cette commande ne fonctionne qu’en mode Videotex.

        Le positionnement avec des caractères deux fois plus hauts se fait par
        rapport au bas du caractère.

        :param largeur:
            coefficiant multiplicateur de largeur (1 ou 2)
        :type largeur:
            un entier

        :param hauteur:
            coefficient multiplicateur de hauteur (1 ou 2)
        :type hauteur:
            un entier
        """
        # assert largeur in [1, 2]
        # assert hauteur in [1, 2]

        # self.envoyer([ESC, 0x4c + (hauteur - 1) + (largeur - 1) * 2])
        ...
