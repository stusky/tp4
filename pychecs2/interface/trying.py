
from pychecs2.interface.interface import Fenetre

class Try(Fenetre):
    def __init__(self):
        super().__init__()

        self.piece_a_deplacer = None
        self.position_piece_a_deplacer = None

    def selectionner(self, event):
        pass
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))



        #Thierry
        try:
            if self.partie.echiquier.couleur_piece_a_position(self.canvas_echiquier.position_selectionnee) == self.partie.echiquier.couleur_piece_a_position(position):
                print('bonne section')
                self.canvas_echiquier.position_selectionnee = None

            if not self.canvas_echiquier.position_selectionnee:
                self.canvas_echiquier.position_selectionnee = position
                if self.partie.echiquier.recuperer_piece_a_position(position) != None:
                    piece = type(self.canvas_echiquier.partie.echiquier.dictionnaire_pieces[position]).__name__
                    print(piece)
                    # On change la valeur de l'attribut position_selectionnee.
                    self.position_selectionnee = position
                    self.messages['text'] = 'Pièce sélectionnée : {} à la position {}.'.format(piece, self.position_selectionnee)
                    self.messages['foreground'] = 'black'


            else:
                self.partie.deplacer(self.canvas_echiquier.position_selectionnee, position)

                self.canvas_echiquier.position_selectionnee = None
                self.liste1.insert(END, self.partie.dernierDeplacement)
                self.liste2.delete(0, END)
                for i in self.partie.gapBlanc:
                    self.liste2.insert(END, i)
                self.liste3.delete(0, END)
                for i in self.partie.gapNoir:
                    self.liste3.insert(END, i)


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
            self.roi_en_rouge()
            if self.canvas_echiquier.position_selectionnee:
                #Mélo, pour ne pas que le carré s'affiche si on séléectionne une pièce adversaire:
                piece_p_s = self.partie.echiquier.recuperer_piece_a_position(self.canvas_echiquier.position_selectionnee)
                if piece_p_s is not None:
                    if piece_p_s.couleur == self.partie.joueur_actif:
                        self.canvas_echiquier.create_rectangle(
                            (event.x // self.canvas_echiquier.n_pixels_par_case) * self.canvas_echiquier.n_pixels_par_case,
                            (event.y // self.canvas_echiquier.n_pixels_par_case) * self.canvas_echiquier.n_pixels_par_case,
                            ((event.x // self.canvas_echiquier.n_pixels_par_case) + 1) * self.canvas_echiquier.n_pixels_par_case,
                            ((event.y // self.canvas_echiquier.n_pixels_par_case) + 1) * self.canvas_echiquier.n_pixels_par_case,
                            fill='pink', tags="select")
            self.canvas_echiquier.raffraichir_pieces()
            self.messages1['text'] = "Au tour du joueur: " + self.partie.joueur_actif.upper()


fenetre = Try()
fenetre.mainloop()











# def selectionner(self, event):
#     # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
#     ligne = event.y // self.canvas_echiquier.n_pixels_par_case
#     colonne = event.x // self.canvas_echiquier.n_pixels_par_case
#     position = "{}{}".format(
#         self.canvas_echiquier.lettres_colonnes[colonne],
#         self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]
#     )
#     self.position = position
#
#     self.roi_en_rouge()
#
#     piece_selectionnee = self.partie.echiquier.recuperer_piece_a_position(position)
#     if piece_selectionnee is not None:
#         print('yes')
#         # Annuler une sélection
#         if piece_selectionnee == self.piece_a_deplacer:
#             print('here you go again')
#             self.piece_a_deplacer = None
#             self.position_piece_a_deplacer = None
#             self.canvas_echiquier.delete('select')
#
#         # Sélection d'une pièce de la couleur du joueur actif
#         elif piece_selectionnee.couleur == self.partie.joueur_actif:
#             self.piece_a_deplacer = piece_selectionnee
#             self.position_piece_a_deplacer = position
#
#             self.messages['text'] = f'Pièce sélectionnée : {self.piece_a_deplacer} à la position {position}.'
#             self.messages['foreground'] = 'black'
#
#             # On supprime les pièces, dessine la case sélectionnée et redessine les pièces
#             self.canvas_echiquier.delete('piece')
#             self.canvas_echiquier.delete('select')
#
#             self.canvas_echiquier.create_rectangle(
#                 (event.x // self.canvas_echiquier.n_pixels_par_case) * self.canvas_echiquier.n_pixels_par_case,
#                 (event.y // self.canvas_echiquier.n_pixels_par_case) * self.canvas_echiquier.n_pixels_par_case,
#                 ((event.x // self.canvas_echiquier.n_pixels_par_case) + 1) * self.canvas_echiquier.n_pixels_par_case,
#                 ((event.y // self.canvas_echiquier.n_pixels_par_case) + 1) * self.canvas_echiquier.n_pixels_par_case,
#                 fill='pink', tags="select")
#
#             self.canvas_echiquier.dessiner_pieces()
#
#         print(self.position)
#         if self.piece_a_deplacer is not None:
#             print('ready to move')
#             print(self.position_piece_a_deplacer, self.position)
#             # if self.partie.echiquier.deplacement_est_valide(self.position_piece_a_deplacer, self.position):
#             #     print('deplace!!')
#             self.partie.echiquier.deplacer(self.position_piece_a_deplacer, position)
#
#             self.canvas_echiquier.raffraichir_cases()