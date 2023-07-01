import turtle

NB_ROWS = 25
NB_COLS = 40

# make screen object and
# set screen mode to world
sc = turtle.Screen()
sc.mode('world')

class Minitel:
    def __init__(self):
        turtle.setworldcoordinates(-3, 103, 103, -3)
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self._draw_frame()
#        self._test_screen()

    def _draw_frame(self):
        self.t.speed(0)
        self.t.width(3)
        self.t.pendown()
        self.t.forward(93.3)
        self.t.left(90)
        self.t.forward(89.6)
        self.t.left(90)
        self.t.forward(93.3)
        self.t.left(90)
        self.t.forward(89.6)
        self.t.penup()

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
        self.t.write(contenu, font=('minitel', 16, 'normal'))

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
        x = (self.current_col - 1) * 2.3 + 0.7
        y = (self.current_row - 1) * 3.5 + 5
        self.t.setposition(x, y)


    def efface(self, portee = 'tout'):
        ...


    def taille(self, largeur: int = 1, hauteur: int = 1):
        ...
