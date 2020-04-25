# -*- coding: utf-8 -*-
"""Ce module contient une classe contenant les informations sur une partie d'échecs,
dont un objet échiquier (une instance de la classe Echiquier).

"""

from pychecs2.echecs.echiquier import Echiquier
from pychecs2.echecs.piece import Roi
import pickle


class AucunePieceAPosition(Exception):
    pass

class MauvaiseCouleurPiece(Exception):
    pass

class Partie:
    """La classe Partie contient les informations sur une partie d'échecs, c'est à dire un échiquier, puis
    un joueur actif (blanc ou noir). Des méthodes sont disponibles pour faire avancer la partie et interagir
    avec l'utilisateur.

    Attributes:
        joueur_actif (str): La couleur du joueur actif, 'blanc' ou 'noir'.
        echiquier (Echiquier): L'échiquier sur lequel se déroule la partie.

    """
    def __init__(self):
        # Le joueur débutant une partie d'échecs est le joueur blanc.
        self.joueur_actif = 'blanc'

        # Création d'une instance de la classe Echiquier, qui sera manipulée dans les méthodes de la classe.
        self.echiquier = Echiquier()

        self.listeDeplacements = []
        self.dernierDeplacement = []

    def determiner_gagnant(self):
        """Détermine la couleur du joueur gagnant, s'il y en a un. Pour déterminer si un joueur est le gagnant,
        le roi de la couleur adverse doit être absente de l'échiquier.

        Returns:
            str: 'blanc' si le joueur blanc a gagné, 'noir' si c'est plutôt le joueur noir, et 'aucun' si aucun
                joueur n'a encore gagné.

        """
        if not self.echiquier.roi_de_couleur_est_dans_echiquier('noir'):
            return 'blanc'
        elif not self.echiquier.roi_de_couleur_est_dans_echiquier('blanc'):
            return 'noir'

        return 'aucun'

    def partie_terminee(self):
        """Vérifie si la partie est terminée. Une partie est terminée si un gagnant peut être déclaré.

        Returns:
            bool: True si la partie est terminée, et False autrement.

        """
        return self.determiner_gagnant() != 'aucun'

    def demander_positions(self):
        """Demande à l'utilisateur d'entrer les positions de départ et d'arrivée pour faire un déplacement. Si les
        positions entrées sont valides (si le déplacement est valide), on retourne les deux positions. On doit
        redemander tant que l'utilisateur ne donne pas des positions valides.

        Returns:
            str, str: Deux chaînes de caractères représentant les deux positions valides fournies par l'utilisateurs.

        """
        while True:
            # On demande et valide la position source.
            while True:
                source = input("Entrez position source: ")
                if self.echiquier.position_est_valide(source) and self.echiquier.couleur_piece_a_position(source) == self.joueur_actif:
                    break

                print("Position invalide.\n")

            # On demande et valide la position cible.
            cible = input("Entrez position cible: ")
            if self.echiquier.deplacement_est_valide(source, cible):
                return source, cible

            print("Déplacement invalide.\n")

    #Thierry
    def deplacer(self, position_source, position_cible):
        piece = self.echiquier.recuperer_piece_a_position(position_source)

        if piece is None:
            raise AucunePieceAPosition("Aucune piece à cet endroit!")
        elif piece.couleur != self.joueur_actif:
            raise MauvaiseCouleurPiece("La pièce source n'appartient pas au joueur actif!")

        self.echiquier.deplacer(position_source, position_cible)
        self.dernierDeplacement = ["(" + piece.couleur + ")" + position_source + "=>" + position_cible]
        self.listeDeplacements.append(self.dernierDeplacement)
        self.joueur_suivant()


    def joueur_suivant(self):
        """Change le joueur actif: passe de blanc à noir, ou de noir à blanc, selon la couleur du joueur actif.

        """
        if self.joueur_actif == 'blanc':
            self.joueur_actif = 'noir'
        else:
            self.joueur_actif = 'blanc'


    def jouer(self):
        """Tant que la partie n'est pas terminée, joue la partie. À chaque tour :
            - On affiche l'échiquier.
            - On demande les deux positions.
            - On fait le déplacement sur l'échiquier.
            - On passe au joueur suivant.

        Une fois la partie terminée, on félicite le joueur gagnant!

        """
        while not self.partie_terminee():
            print(self.echiquier)
            print("\nAu tour du joueur {}".format(self.joueur_actif))
            source, cible = self.demander_positions()
            self.echiquier.deplacer(source, cible)
            self.joueur_suivant()

        print(self.echiquier)
        print("\nPartie terminée! Le joueur {} a gagné".format(self.determiner_gagnant()))

    def position_mon_roi(self, couleur_joueur_actif):
        for position in self.echiquier.dictionnaire_pieces.keys():
            if isinstance(self.echiquier.dictionnaire_pieces[position], Roi) \
                    and self.echiquier.dictionnaire_pieces[position].couleur == couleur_joueur_actif:
                return position

    # Mélo
    def mon_roi_en_echec(self):
        if self.joueur_actif == 'blanc':
            autre_couleur = 'noir'
        else:
            autre_couleur = 'blanc'

        return self.echiquier.case_est_menacee_par(self.position_mon_roi, autre_couleur)

    def sauvegarder_partie(self):
        """
        """
        with open("sauvegarde", "wb") as f:
            pickle.dump(self.echiquier.dictionnaire_pieces, f)
        #TODO documenter la méthode


    def charger_partie(self):
        """
        """
        with open("sauvegarde", "rb") as f:
            self.echiquier.dictionnaire_pieces = pickle.load(f)
        # TODO documenter la méthode



# aa = ['(blanc)f2=>f4', '(noir)d7=>d5']
# print(', '.join(aa))
#
# dernierDeplacement = ("(" + piece.couleur + ")" + position_source + "=>" + position_cible])

if __name__ == '__main__':
    pass
