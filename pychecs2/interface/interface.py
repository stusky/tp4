"""Solution du laboratoire, permettant de bien comprendre comment hériter d'un widget de tkinter, de dessiner
un échiquier dans un Canvas, puis de déterminer quelle case a été sélectionnée.

"""
from tkinter import NSEW, Canvas, Label, Tk, Button, LabelFrame, RIDGE, Listbox, END, Scrollbar, RIGHT, Y, LEFT, VERTICAL, N, S, E, W, Frame
import webbrowser
from pychecs2.echecs.partie import AucunePieceAPosition, MauvaiseCouleurPiece
from pychecs2.echecs.echiquier import Echiquier, ErreurDeplacement

# Exemple d'importation de la classe Partie.
from pychecs2.echecs.partie import Partie
from pychecs2.echecs.echiquier import Echiquier



class CanvasEchiquier(Canvas):
    """Classe héritant d'un Canvas, et affichant un échiquier qui se redimensionne automatique lorsque
    la fenêtre est étirée.

    """
    def __init__(self, parent, n_pixels_par_case, partie):
        # Nombre de lignes et de colonnes.
        self.n_lignes = 8
        self.n_colonnes = 8

        # Noms des lignes et des colonnes.
        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


        # La position sélectionnée.
        self.position_selectionnee = None

        self.partie = partie


        # Nombre de pixels par case, variable.
        self.n_pixels_par_case = n_pixels_par_case

        # Appel du constructeur de la classe de base (Canvas).
        # La largeur et la hauteur sont déterminés en fonction du nombre de cases.
        super().__init__(parent, width=self.n_lignes * n_pixels_par_case,
                         height=self.n_colonnes * self.n_pixels_par_case)

        # Dictionnaire contenant les pièces. Vous devinerez, si vous réutilisez cette classe dans votre TP4,
        # qu'il fandra adapter ce code pour plutôt utiliser la classe Echiquier.

        # self.pieces = {
        #     'a1': 'TB', 'b1': 'CB', 'c1': 'FB', 'd1': 'DB', 'e1': 'RB', 'f1': 'FB', 'g1': 'CB', 'h1': 'TB',
        #     'a2': 'PB', 'b2': 'PB', 'c2': 'PB', 'd2': 'PB', 'e2': 'PB', 'f2': 'PB', 'g2': 'PB', 'h2': 'PB',
        #     'a7': 'PN', 'b7': 'PN', 'c7': 'PN', 'd7': 'PN', 'e7': 'PN', 'f7': 'PN', 'g7': 'PN', 'h7': 'PN',
        #     'a8': 'TN', 'b8': 'CN', 'c8': 'FN', 'd8': 'DN', 'e8': 'RN', 'f8': 'FN', 'g8': 'CN', 'h8': 'TN',
        # }



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
        for position, piece in self.partie.echiquier.dictionnaire_pieces.items():
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.
            coordonnee_y = (self.n_lignes - self.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            coordonnee_x = self.lettres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            self.create_text(coordonnee_x, coordonnee_y, text= piece,
                             font=('Deja Vu', self.n_pixels_par_case//2), tags='piece')


    def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.n_lignes

        self.raffraichir_cases()
        self.raffraichir_pieces()

    #Thierry
    def raffraichir_pieces(self):
        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('piece')
        self.dessiner_pieces()

    def raffraichir_cases(self):
        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('case')
        self.dessiner_cases()


class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("Échiquier")


        self.partie = Partie()


        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création du canvas échiquier.
        self.canvas_echiquier = CanvasEchiquier(self, 60, self.partie)
        self.canvas_echiquier.grid(sticky=NSEW)

        ##########################################################
        #                                                        #
        #                    VISUEL                              #
        #                                                        #
        ##########################################################
        # Étiquette d'information et de sélection des pièces
        self.messages = Label(self)
        self.messages['foreground'] = 'black'
        self.messages['text'] = "Bienvenue au super jeux d'échec!"
        self.messages.grid(row=1, sticky = 'w')

        # # Étiquette d'information sur le joueur courant
        self.messages1 = Label(self)
        self.messages1['text'] = "Au tour du joueur: " + self.partie.joueur_actif.upper()
        self.messages1.grid(row=2, sticky = 'w')
        self.messages1['foreground'] = 'blue'

        # Fenetre pour afficher la liste des déplacements effectués
        self.monFramePrincipal = Frame(self)
        self.monFramePrincipal.grid(row=0, column=1, sticky='n')
        self.mon_frame1 = LabelFrame(self.monFramePrincipal, text="Les déplacements ", borderwidth=2, relief=RIDGE, padx=5, pady=5)
        self.mon_frame1.grid(row=0, column=0, sticky='n')
        self.yScroll = Scrollbar(self.mon_frame1, orient=VERTICAL)
        self.yScroll.grid(row=0, column=1, sticky=N + S)
        self.liste1 = Listbox(self.mon_frame1, yscrollcommand=self.yScroll.set)
        self.liste1 = Listbox(self.mon_frame1)
        self.liste1.grid(row=0, column=0)
        self.yScroll['command'] = self.liste1.yview
        self.mon_frame2 = Frame(self.monFramePrincipal, borderwidth=2, relief=RIDGE, padx=5, pady=5)
        self.mon_frame2.grid(row=2, column=0, sticky='n')
        but1 = Button(self.mon_frame2, text="Lien web pour accéder\naux règles du jeu!", command=self.ouvrirURL).grid(row=0, column=0)



        # Frame pour les options de jeux
        self.mon_frame = LabelFrame(self, text="Options de jeux", borderwidth=2, relief=RIDGE, padx=5, pady=5)
        self.mon_frame.grid(row=4, column=0, sticky = 'w')
        bouton_sauver = Button(self.mon_frame, text="Sauvegarder une partie", command = self.sauvergarder).grid(row=0, column=0)
        bouton_charge = Button(self.mon_frame, text="Charger une partie", command = self.charger).grid(row=0, column=1)
        bouton_demarrer = Button(self.mon_frame, text="Démarrer une nouvelle partie", command=self.reinitialiser).grid(row=0, column=2)


        # On lie un clic sur le CanvasEchiquier à une méthode.
        self.canvas_echiquier.bind('<Button-1>', self.selectionner)

        #Mélo (dans sélectionner?)
           # if self.partie.mon_roi_en_echec:
    #     self.roi_en_rouge()

    def ouvrirURL(self):
        url = 'https://fr.wikipedia.org/wiki/Règles_du_jeu_d%27échecs'
        webbrowser.open_new(url)

    def reinitialiser(self):
        self.partie.echiquier.initialiser_echiquier_depart()
        self.canvas_echiquier.raffraichir_cases()
        self.canvas_echiquier.raffraichir_pieces()

    def sauvergarder(self):
        self.partie.sauvegarder_partie()
        self.canvas_echiquier.raffraichir_cases()
        self.canvas_echiquier.raffraichir_pieces()

    def charger(self):
        self.partie.charger_partie()
        self.canvas_echiquier.raffraichir_cases()
        self.canvas_echiquier.raffraichir_pieces()

    def selectionner(self, event):
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))



        #Thierry
        try:
            if self.partie.echiquier.couleur_piece_a_position(self.canvas_echiquier.position_selectionnee) == self.partie.echiquier.couleur_piece_a_position(position):
                self.canvas_echiquier.position_selectionnee = None

            if not self.canvas_echiquier.position_selectionnee:
                self.canvas_echiquier.position_selectionnee = position
                if self.partie.echiquier.recuperer_piece_a_position(position) != None:
                    piece = type(self.canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]).__name__

                    # On change la valeur de l'attribut position_selectionnee.
                    self.position_selectionnee = position
                    self.messages['text'] = 'Pièce sélectionnée : {} à la position {}.'.format(piece, self.position_selectionnee)


            else:
                self.partie.deplacer(self.canvas_echiquier.position_selectionnee, position)
                self.canvas_echiquier.position_selectionnee = None
                self.liste1.insert(END, self.partie.dernierDeplacement)

                if self.partie.partie_terminee():
                    self.messages['foreground'] = 'green'
                    self.messages['text'] = 'Partie terminée, les ' + self.partie.determiner_gagnant().upper() + ' ont gagné.\nOn recommence?!'

        except (ErreurDeplacement, AucunePieceAPosition, MauvaiseCouleurPiece) as e:
            self.messages['foreground'] = 'red'
            self.messages['text'] = e
            self.canvas_echiquier.position_selectionnee = None


        #Thierry
        finally:
            self.canvas_echiquier.raffraichir_cases()
            if self.canvas_echiquier.position_selectionnee:
                self.canvas_echiquier.create_rectangle(
                    (event.x // self.canvas_echiquier.n_pixels_par_case) * self.canvas_echiquier.n_pixels_par_case,
                    (event.y // self.canvas_echiquier.n_pixels_par_case) * self.canvas_echiquier.n_pixels_par_case,
                    ((event.x // self.canvas_echiquier.n_pixels_par_case) + 1) * self.canvas_echiquier.n_pixels_par_case,
                    ((event.y // self.canvas_echiquier.n_pixels_par_case) + 1) * self.canvas_echiquier.n_pixels_par_case,
                    fill='pink', tags="select")
            self.canvas_echiquier.raffraichir_pieces()
            self.messages1['text'] = "Au tour du: " + self.partie.joueur_actif.upper()

    #Mélo
    def roi_en_rouge(self, event):
        #
        # self.canvas_echiquier.raffraichir_cases()
        # if self.canvas_echiquier.partie.mon_roi_en_echec():
        #     self.canvas_echiquier.create_rectangle(
        #         (event.x // self.canvas_echiquier.n_pixels_par_case) * self.canvas_echiquier.n_pixels_par_case,
        #         (event.y // self.canvas_echiquier.n_pixels_par_case) * self.canvas_echiquier.n_pixels_par_case,
        #         ((event.x // self.canvas_echiquier.n_pixels_par_case) + 1) * self.canvas_echiquier.n_pixels_par_case,
        #         ((event.y // self.canvas_echiquier.n_pixels_par_case) + 1) * self.canvas_echiquier.n_pixels_par_case,
        #         fill='red')
        pass


        # On récupère l'information sur la pièce à l'endroit choisi. Notez le try...except!
        #Thierry
        # try:
        #     piece = type(self.canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]).__name__
        #
        #     # On change la valeur de l'attribut position_selectionnee.
        #     self.position_selectionnee = position
        #
        #     self.messages['foreground'] = 'black'
        #     self.messages['text'] = 'Pièce sélectionnée : {} à la position {}.'.format(piece, self.position_selectionnee)
        #
        # except KeyError:
        #     self.messages['foreground'] = 'red'
        #     self.messages['text'] = 'Erreurzzz: Aucune pièce à cet endroit.'
        #     self.canvas_echiquier.position_selectionnee = None
