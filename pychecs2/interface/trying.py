
from pychecs2.interface.interface import Fenetre

class Try(Fenetre):
    def __init__(self):
        super().__init__()

        self.piece_a_deplacer = None
        self.position_piece_a_deplacer = None



    def selectionner(self, event):
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(
            self.canvas_echiquier.lettres_colonnes[colonne],
            self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]
        )
        self.position = position

        self.roi_en_rouge()

        piece_selectionnee = self.partie.echiquier.recuperer_piece_a_position(position)
        if piece_selectionnee is not None:
            print('yes')
            #Annuler une sélection
            if piece_selectionnee == self.piece_a_deplacer:
                print('here you go again')
                self.piece_a_deplacer = None
                self.position_piece_a_deplacer = None
                self.canvas_echiquier.delete('select')

            #Sélection d'une pièce de la couleur du joueur actif
            elif piece_selectionnee.couleur == self.partie.joueur_actif:
                self.piece_a_deplacer = piece_selectionnee
                self.position_piece_a_deplacer = position

                self.messages['text'] = f'Pièce sélectionnée : {self.piece_a_deplacer} à la position {position}.'
                self.messages['foreground'] = 'black'

                #On supprime les pièces, dessine la case sélectionnée et redessine les pièces
                self.canvas_echiquier.delete('piece')
                self.canvas_echiquier.delete('select')

                self.canvas_echiquier.create_rectangle(
                    (event.x // self.canvas_echiquier.n_pixels_par_case) * self.canvas_echiquier.n_pixels_par_case,
                    (event.y // self.canvas_echiquier.n_pixels_par_case) * self.canvas_echiquier.n_pixels_par_case,
                    ((event.x // self.canvas_echiquier.n_pixels_par_case) + 1) * self.canvas_echiquier.n_pixels_par_case,
                    ((event.y // self.canvas_echiquier.n_pixels_par_case) + 1) * self.canvas_echiquier.n_pixels_par_case,
                    fill='pink', tags="select")

                self.canvas_echiquier.dessiner_pieces()

            print(self.position)
            if self.piece_a_deplacer is not None:
                print('ready to move')
                print(self.position_piece_a_deplacer, self.position)
                # if self.partie.echiquier.deplacement_est_valide(self.position_piece_a_deplacer, self.position):
                #     print('deplace!!')
                self.partie.echiquier.deplacer(self.position_piece_a_deplacer, position)

                self.canvas_echiquier.raffraichir_cases()



        # if self.piece_a_deplacer is not None:
        #     print('yessir miller')
        #



fenetre = Try()
fenetre.mainloop()