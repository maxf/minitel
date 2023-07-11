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
#        self.font = pg.font.Font(f'{location}/caracteres_semigraphiques.ttf', 80)

        # initial text position
        self.current_col = 1
        self.current_row = 1

        pg.draw.rect(self.screen, (0,0,0), pg.Rect(100,50, 1600, 50*NB_ROWS))


#        self.test_screen()

    def test_screen(self):
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


    def _pos_to_xy(self, pos):
        return (
            (pos[0] - 1)*40+100,
            (pos[1] - 1)*50+50
        )



    def _envoyer_un_caractere(self, char):
        ren = self.font.render(char, 0, self.fg, self.bg)

        #x = (self.current_col - 1) * 40 + 100
        #y = (self.current_row - 1) * 50 + 50
        (x, y) = self._pos_to_xy((self.current_col, self.current_row))

        # when a double character won't fit, minitel resets
        # the scale to 1
        actual_scale_x = self.scale_x
        if self.scale_x == 2 and self.current_col == NB_COLS:
            actual_scale_x = 1

        if self.scale_y == 2 and self.current_row == 1:
            self.scale_x = 1
            self.scale_y = 1

        ren = pg.transform.scale_by(ren, (actual_scale_x, self.scale_y))

        if self.scale_y == 2:
            y = y - 50

        self.screen.blit(ren, (x, y))
        pg.display.flip()

        # Calculate the next cursor position

        # NORMAL SIZE CHARS (1,1)
        if self.scale_x == 1 and self.scale_y == 1:
            if self.current_col < NB_COLS:
                self.current_col = self.current_col + 1
            else:
                self.current_col = 1
                if self.current_row < NB_ROWS:
                    self.current_row = self.current_row + 1
                else:
                    self.current_row = 1

        # DOUBLE SIZE CHARS (2,2)
        if self.scale_x == 2 and self.scale_y == 2:
            if self.current_col < NB_COLS-1:
                self.current_col = self.current_col + 2
            elif self.current_col == NB_COLS - 1:
                self.current_col = self.current_col + 1
            else:
                self.current_col = 1
                if self.current_row < NB_ROWS-2:
                    self.current_row = self.current_row + 2
                else:
                    self.current_row = 1

        # DOUBLE HEIGHT CHARS (1,2)
        if self.scale_x == 1 and self.scale_y == 2:
            if self.current_col < NB_COLS:
                self.current_col = self.current_col + 1
            else:
                self.current_col = 1
                if self.current_row < NB_ROWS-2:
                    self.current_row = self.current_row + 2
                else:
                    self.current_row = 1

        # (newx, newy) = self._pos_to_xy((self.current_col, self.current_row))
        #  pg.draw.rect(self.screen, (255,0,0), pg.Rect(newx,newy+200, 10, 10))
        #  pg.display.flip()



        # if self.scale_x != 1 or self.scale_y != 1:
        #     ren = pg.transform.scale_by(ren, (self.scale_x, self.scale_y))
        #     if self.scale_y == 2:
        #         y = y - 50

        # if self.scale_x == 1 and self.scale_x == 1:
        #     if self.current_col == NB_COLS:
        #         self.current_col = 1
        #         if self.current_row == NB_ROWS:
        #             self.current_row = 1
        #         else:
        #             self.current_row = self.current_row + 1
        #     else:
        #         self.current_col = self.current_col + 1

        # if self.scale_x == 2 and self.scale_x == 2:
        #     if self.current_col == NB_COLS:
        #         self.current_col = 1
        #         if self.current_row == NB_ROWS:
        #             self.current_row = 1
        #         else:
        #             self.current_row = self.current_row + 2
        #     else:
        #         self.current_col = self.current_col + 2




    def envoyer(self, contenu):
        """Envoi de séquence de caractères

        Envoie une séquence de caractère en direction du Minitel.

        :param contenu:
            Une séquence de caractères interprétable par la classe Sequence.
        :type contenu:
            un objet Sequence, une chaîne de caractères ou unicode, une liste,
            un entier
        """
        for char in contenu:
            self._envoyer_un_caractere(char)

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

        self.taille(1,1) # For some reason, position() resets the taille




    def efface(self, portee = 'tout'):
        pg.draw.rect(self.screen, (0,0,0), pg.Rect(100,50, 1600, 50*NB_ROWS))


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
