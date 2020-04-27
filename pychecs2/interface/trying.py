
from pychecs2.interface.interface import CanvasEchiquier, Fenetre
from pychecs2.echecs.partie import Partie
from pychecs2.echecs.echiquier import Echiquier


class Try(Fenetre):
    def __init__(self):
        super().__init__()

        self.roi_en_rouge()

    def roi_en_rouge(self):

        if self.partie.mon_roi_en_echec():
            #On supprime les pieces et les cases
            self.canvas_echiquier.delete('case')
            self.canvas_echiquier.delete('piece')

            #On determine la position du Roi en échec:
            position_roi = self.partie.position_mon_roi(self.partie.joueur_actif)

            #Écriture de la case du roi en pixels
            index_colonne = self.echichier.lettres_colonnes.index(position_roi[0])
            coordonnees_x1 = index_colonne * self.canvas_echiquier.n_pixels_par_case
            coordonnees_x2 = coordonnees_x1 + self.canvas_echiquier.n_pixels_par_case

            coordonnees_y1 = (7 - self.echichier.chiffre_rangees.index(position_roi[1])) * self.canvas_echiquier.n_pixels_par_case
            coordonnees_y2 = coordonnees_y1 + self.canvas_echiquier.n_pixels_par_case

            #On redessine les cases
            self.canvas_echiquier.dessiner_cases()

            #Dessin du carré rouge
            self.canvas_echiquier.create_rectangle(
                coordonnees_x1, coordonnees_y1, coordonnees_x2, coordonnees_y2, fill='red'
            )
            #On redessine les pieces
            self.canvas_echiquier.dessiner_pieces()



if __name__ == '__main__':


    test = Try()
    test.mainloop()