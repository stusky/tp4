"""Solution du laboratoire, permettant de bien comprendre comment hériter d'un widget de tkinter, de dessiner
un échiquier dans un Canvas, puis de déterminer quelle case a été sélectionnée.

"""
from tkinter import NSEW, Canvas, Label, Tk, Frame, Button
import json

# Exemple d'importation de la classe Partie.
from pychecs2.echecs.partie import Partie


class CanvasEchiquier(Canvas):
    """Classe héritant d'un Canvas, et affichant un échiquier qui se redimensionne automatique lorsque
    la fenêtre est étirée.

    """
    def __init__(self, parent, n_pixels_par_case):
        # Nombre de lignes et de colonnes.
        self.n_lignes = 8
        self.n_colonnes = 8

        # Noms des lignes et des colonnes.
        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Nombre de pixels par case, variable.
        self.n_pixels_par_case = n_pixels_par_case

        # Appel du constructeur de la classe de base (Canvas).
        # La largeur et la hauteur sont déterminés en fonction du nombre de cases.
        super().__init__(parent, width=self.n_lignes * n_pixels_par_case,
                         height=self.n_colonnes * self.n_pixels_par_case)

        # Dictionnaire contenant les pièces. Vous devinerez, si vous réutilisez cette classe dans votre TP4,
        # qu'il fandra adapter ce code pour plutôt utiliser la classe Echiquier.
        #self.pieces = {
        #    'a1': 'TB', 'b1': 'CB', 'c1': 'FB', 'd1': 'DB', 'e1': 'RB', 'f1': 'FB', 'g1': 'CB', 'h1': 'TB',
        #    'a2': 'PB', 'b2': 'PB', 'c2': 'PB', 'd2': 'PB', 'e2': 'PB', 'f2': 'PB', 'g2': 'PB', 'h2': 'PB',
        #    'a7': 'PN', 'b7': 'PN', 'c7': 'PN', 'd7': 'PN', 'e7': 'PN', 'f7': 'PN', 'g7': 'PN', 'h7': 'PN',
        #    'a8': 'TN', 'b8': 'CN', 'c8': 'FN', 'd8': 'DN', 'e8': 'RN', 'f8': 'FN', 'g8': 'CN', 'h8': 'TN',
        #}

        #Thierry
        self.partie = Partie()

        # On fait en sorte que le redimensionnement du canvas redimensionne son contenu. Cet événement étant également
        # généré lors de la création de la fenêtre, nous n'avons pas à dessiner les cases et les pièces dans le
        # constructeur.
        self.bind('<Configure>', self.redimensionner)

    def dessiner_cases(self):
        """Méthode qui dessine les cases de l'échiquier.

        """
        for i in range(self.n_lignes):
            for j in range(self.n_colonnes):
                debut_ligne = i * self.n_pixels_par_case
                fin_ligne = debut_ligne + self.n_pixels_par_case
                debut_colonne = j * self.n_pixels_par_case
                fin_colonne = debut_colonne + self.n_pixels_par_case

                # On détermine la couleur.
                if (i + j) % 2 == 0:
                    couleur = 'white'
                else:
                    couleur = 'gray'

                # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer les éléments
                # par la suite.
                self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill=couleur, tags='case')

    def dessiner_pieces(self):
        # Caractères unicode représentant les pièces. Vous avez besoin de la police d'écriture DejaVu.
        caracteres_pieces = {'PB': '\u2659',
                             'PN': '\u265f',
                             'TB': '\u2656',
                             'TN': '\u265c',
                             'CB': '\u2658',
                             'CN': '\u265e',
                             'FB': '\u2657',
                             'FN': '\u265d',
                             'RB': '\u2654',
                             'RN': '\u265a',
                             'DB': '\u2655',
                             'DN': '\u265b'
                             }

        # Pour tout paire position, pièce:

        #Thierry
        for position, piece in self.partie.echiquier.dictionnaire_pieces.items():
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.
            coordonnee_y = (self.n_lignes - self.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            coordonnee_x = self.lettres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            self.create_text(coordonnee_x, coordonnee_y, text= piece,#Thierry caracteres_pieces[piece],
                             font=('Deja Vu', self.n_pixels_par_case//2), tags='piece')

    def redimensionner(self, event=None):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.

        if(event is not None):
            nouvelle_taille = min(event.width, event.height)

            # Calcul de la nouvelle dimension des cases.
            self.n_pixels_par_case = nouvelle_taille // self.n_lignes

        # On supprime les anciennes cases et on ajoute les nouvelles.
        self.delete('case')
        self.dessiner_cases()

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('piece')
        self.dessiner_pieces()

    def rejouer(self):
        self.partie = Partie()
        self.redimensionner()


class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("Échiquier")

        # La position sélectionnée.
        self.position_selectionnee = None

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création du canvas échiquier.
        self.canvas_echiquier = CanvasEchiquier(self, 60)
        self.canvas_echiquier.grid(row=0, sticky=NSEW)

        cadre_boutons = Frame(self)
        cadre_boutons.grid(row=1, sticky=NSEW)

        self.bouton_rejouer =  Button(cadre_boutons, text="rejouer", command=self.rejouer)
        self.bouton_rejouer.grid(row=0, column=0)
        self.bouton_sauvegarder =  Button(cadre_boutons, text="sauvegarder", command=self.sauvegarder)
        self.bouton_sauvegarder.grid(row=0, column=1)
        self.bouton_charger =  Button(cadre_boutons, text="charger", command=self.charger)
        self.bouton_charger.grid(row=0, column=2)


        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # On lie un clic sur le CanvasEchiquier à une méthode.
        self.canvas_echiquier.bind('<Button-1>', self.selectionner)

        self.messages['foreground'] = 'black'
        self.messages['text'] = 'Les blancs commencent'

    def rejouer(self):
        self.canvas_echiquier.rejouer()
        self.messages['foreground'] = 'black'
        self.messages['text'] = 'Les blancs commencent'

    #Thierry
    def sauvegarder(self):
        self.canvas_echiquier.partie.sauvegarder()

    #Thierry
    def charger(self):
        self.canvas_echiquier.partie.charger()
        self.canvas_echiquier.redimensionner()

    def selectionner(self, event):

        #Thierry
        if(self.canvas_echiquier.partie.partie_terminee()):
            self.messages['foreground'] = 'red'
            self.messages['text'] = "La partie est terminee. Appuyer sur le bouton rejouer pour demarrer une nouvelle partie"
            return

        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))

        #Thierry
        if self.position_selectionnee is None or self.canvas_echiquier.partie.echiquier.couleur_piece_a_position(position) == self.canvas_echiquier.partie.joueur_actif:
            # On récupère l'information sur la pièce à l'endroit choisi. Notez le try...except!

            #Thierry
            couleur = self.canvas_echiquier.partie.echiquier.couleur_piece_a_position(position)
            if(couleur != '' and couleur != self.canvas_echiquier.partie.joueur_actif):
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'La couleur de la piece selectionnee ne correspond pas a la couleur du joueur actuel!'
            else:
                try:
                    piece = self.canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]

                    # On change la valeur de l'attribut position_selectionnee.
                    self.position_selectionnee = position

                    self.messages['foreground'] = 'black'
                    self.messages['text'] = 'Pièce sélectionnée : {} à la position {}.'.format(piece, self.position_selectionnee)

                except KeyError:
                    self.messages['foreground'] = 'red'
                    self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'

        else:
            try:
                #Thierry
                self.canvas_echiquier.partie.jouerEtape(self.position_selectionnee, position)
            except ValueError as e:

                #Thierry
                self.messages['foreground'] = 'red'
                #self.messages['text'] = 'Erreur: La piece na pas pu etre deplacee.'
                self.messages['text'] = e
            else:

                #Thierry
                self.canvas_echiquier.redimensionner()

                #Thierry
                if(self.canvas_echiquier.partie.partie_terminee()):
                    self.messages['foreground'] = 'green'
                    self.messages['text'] = "Partie terminée! Le joueur {} a gagné".format(self.canvas_echiquier.partie.determiner_gagnant())
                else:
                    self.messages['foreground'] = 'black'
                    self.messages['text'] = 'Au tour des {}s de jouer'.format(self.canvas_echiquier.partie.joueur_actif)

            self.position_selectionnee = None