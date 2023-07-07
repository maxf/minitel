import pygame as pg
import os

NB_ROWS = 25
NB_COLS = 40

pg.init()

class Minitel:
    def __init__(self):
        pg.init()
        resolution = 1800, 1400
        self.screen = pg.display.set_mode(resolution)
        self.fg = 250, 240, 230
        self.bg = 5, 5, 5
        self.scale_x = 1
        self.scale_y = 1
        wincolor = 40, 40, 90
        self.screen.fill(wincolor)
        current_dir = os.path.abspath(__file__)
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.font = pg.font.Font(f'{location}/Minitel.ttf', 40)

        self._test_screen()

    def _test_screen(self):
        for row in range(1, NB_ROWS+1):
            for col in range(1, NB_COLS+1):
                self.position(col, row)
                self.envoyer('X')

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
        """Envoi de séquence de caractères

        Envoie une séquence de caractère en direction du Minitel.

        :param contenu:
            Une séquence de caractères interprétable par la classe Sequence.
        :type contenu:
            un objet Sequence, une chaîne de caractères ou unicode, une liste,
            un entier
        """
        ren = self.font.render(contenu, 0, self.fg, self.bg)

        if self.scale_x != 1 or self.scale_y != 1:
            ren = pg.transform.scale_by(ren, (self.scale_x, self.scale_y))

        x = (self.current_col - 1) * 40 + 100
        y = (self.current_row - 1) * 50 + 50

        self.screen.blit(ren, (x, y))
        pg.display.flip()

    def recevoir(self, bloque = False, attente = None):
        ...

    def position(self, colonne, ligne, relatif = False):
        """Définit la position du curseur du Minitel

        Note:
        Cette méthode optimise le déplacement du curseur, il est donc important
        de se poser la question sur le mode de positionnement (relatif vs
        absolu) car le nombre de caractères générés peut aller de 1 à 5.

        Sur le Minitel, la première colonne a la valeur 1. La première ligne
        a également la valeur 1 bien que la ligne 0 existe. Cette dernière
        correspond à la ligne d’état et possède un fonctionnement différent
        des autres lignes.

        :param colonne:
            colonne à laquelle positionner le curseur
        :type colonne:
            un entier relatif

        :param ligne:
            ligne à laquelle positionner le curseur
        :type ligne:
            un entier relatif

        :param relatif:
            indique si les coordonnées fournies sont relatives
            (True) par rapport à la position actuelle du curseur ou si
            elles sont absolues (False, valeur par défaut)
        :type relatif:
            un booléen
        """
        self.current_col = colonne
        self.current_row = ligne



    def efface(self, portee = 'tout'):
        ...


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
        assert largeur in [1, 2]
        assert hauteur in [1, 2]

        self.scale_x = largeur
        self.scale_y = hauteur
