# -*- coding: utf-8 -*-
"""Ce module contient une classe contenant les informations sur une partie d'échecs,
dont un objet échiquier (une instance de la classe Echiquier).

"""
from pychecs2.echecs.echiquier import Echiquier
from pychecs2.echecs.piece import Roi, Tour, Pion, Dame, Fou, Cavalier
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

        # self.gapBlanc = None
        # self.gapNoir = None

        self.hist = []

        self.nom_fichier_sauvegarde= 'sauvegarde'

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

    def annulerDernierMouvement(self):
        # self.echiquier.dictionnaire_pieces = self.echiquier.listeDesEchiquiers[-2]

        if len(self.echiquier.listeDesEchiquiers) <= 2:
            self.echiquier.initialiser_echiquier_depart()
            self.joueur_actif = 'blanc'

        else:
            del self.echiquier.listeDesEchiquiers[-1]
            self.echiquier.dictionnaire_pieces = self.echiquier.listeDesEchiquiers[-1]
            self.joueur_suivant()


        self.resteBlanc = set()
        self.resteNoir = set()
        for i in self.echiquier.dictionnaire_pieces.values():
            if i.est_blanc():
                self.resteBlanc.add(i)
            else:
                self.resteNoir.add(i)
        self.gapBlanc = list(self.echiquier.setBlanc - self.resteBlanc)
        self.gapNoir = list(self.echiquier.setNoir - self.resteNoir)

    # Mélo
    def roque_est_valide(self, position_source, position_cible):
        couleur_adversaire = 'blanc'
        rangee_origine = '8'

        piece = self.echiquier.recuperer_piece_a_position(position_source)
        piece_cible = self.echiquier.recuperer_piece_a_position(position_cible)

        if piece.couleur == 'blanc':
            couleur_adversaire = 'noir'
            rangee_origine = '1'

        if isinstance(piece, Roi) and isinstance(piece_cible, Tour) and\
                piece.couleur == piece_cible.couleur and\
                self.echiquier.recuperer_piece_a_position(position_source) not in self.hist and \
                self.echiquier.recuperer_piece_a_position(position_cible) not in self.hist:
            if position_cible[0] == 'a':
                for colonne in self.echiquier.lettres_colonnes[0:5]:

                    if self.echiquier.case_est_menacee_par(colonne + rangee_origine, couleur_adversaire):
                        return False
                return True
            else:
                for colonne in self.echiquier.lettres_colonnes[4:]:
                    if self.echiquier.case_est_menacee_par(colonne + rangee_origine, couleur_adversaire):
                        return False
                return True

    def roquer(self, position_source, position_cible):

        self.joueur_suivant()
        if ord(position_source[0]) > ord(position_cible[0]):
            position_roi = 'c' + position_source[1]
            self.echiquier.dictionnaire_pieces[position_roi] = \
                self.echiquier.recuperer_piece_a_position(position_source)
            del self.echiquier.dictionnaire_pieces[position_source]

            position_tour = 'd' + position_cible[1]
            self.echiquier.dictionnaire_pieces[position_tour] = \
                self.echiquier.recuperer_piece_a_position(position_cible)
            del self.echiquier.dictionnaire_pieces[position_cible]
        else:
            position_roi = 'g' + position_source[1]
            self.echiquier.dictionnaire_pieces[position_roi] = \
                self.echiquier.recuperer_piece_a_position(position_source)
            del self.echiquier.dictionnaire_pieces[position_source]

            position_tour = 'f' + position_cible[1]
            self.echiquier.dictionnaire_pieces[position_tour] = \
                self.echiquier.recuperer_piece_a_position(position_cible)
            del self.echiquier.dictionnaire_pieces[position_cible]



        #Trucs a Thierry
        piece = self.echiquier.recuperer_piece_a_position(position_source)
        self.dernierDeplacement = ["(" + self.joueur_actif + ")" + position_source + "->" + position_cible]
        self.listeDeplacements.append(self.dernierDeplacement)


        echiquierCopy = dict(self.echiquier.dictionnaire_pieces)
        self.echiquier.listeDesEchiquiers.append(echiquierCopy)

        self.resteBlanc = set()
        self.resteNoir = set()
        for i in self.echiquier.dictionnaire_pieces.values():
            if (i.est_blanc()):
                self.resteBlanc.add(i)
            else:
                self.resteNoir.add(i)

        self.gapBlanc = list(self.echiquier.setBlanc - self.resteBlanc)
        self.gapNoir = list(self.echiquier.setNoir - self.resteNoir)

    #Thierry
    def deplacer(self, position_source, position_cible):
        piece = self.echiquier.recuperer_piece_a_position(position_source)

        #Pour le roque
        if self.echiquier.deplacement_est_valide(position_source, position_cible):
            self.hist.append(piece)

        self.echiquier.deplacer(position_source, position_cible)

        self.joueur_suivant()
        self.dernierDeplacement = ["(" + piece.couleur + ")" + position_source + "->" + position_cible]
        self.listeDeplacements.append(self.dernierDeplacement)

        echiquierCopy = dict(self.echiquier.dictionnaire_pieces)
        self.echiquier.listeDesEchiquiers.append(echiquierCopy)

        self.dictionnaire_pieces_initial = {
            'a1': Tour('blanc'),
            'b1': Cavalier('blanc'),
            'c1': Fou('blanc'),
            'd1': Dame('blanc'),
            'e1': Roi('blanc'),
            'f1': Fou('blanc'),
            'g1': Cavalier('blanc'),
            'h1': Tour('blanc'),
            'a2': Pion('blanc'),
            'b2': Pion('blanc'),
            'c2': Pion('blanc'),
            'd2': Pion('blanc'),
            'e2': Pion('blanc'),
            'f2': Pion('blanc'),
            'g2': Pion('blanc'),
            'h2': Pion('blanc'),
            'a7': Pion('noir'),
            'b7': Pion('noir'),
            'c7': Pion('noir'),
            'd7': Pion('noir'),
            'e7': Pion('noir'),
            'f7': Pion('noir'),
            'g7': Pion('noir'),
            'h7': Pion('noir'),
            'a8': Tour('noir'),
            'b8': Cavalier('noir'),
            'c8': Fou('noir'),
            'd8': Dame('noir'),
            'e8': Roi('noir'),
            'f8': Fou('noir'),
            'g8': Cavalier('noir'),
            'h8': Tour('noir'),
        }

        self.setBlanc = set()
        self.setNoir = set()
        for i in self.dictionnaire_pieces_initial.values():
            if i.est_blanc():
                self.setBlanc.add(i)
            else:
                self.setNoir.add(i)

        self.resteBlanc = set()
        self.resteNoir = set()
        for i in self.echiquier.dictionnaire_pieces.values():
            if i.est_blanc():
                self.resteBlanc.add(i)
            else:
                self.resteNoir.add(i)


        self.gapBlanc = list(self.echiquier.setBlanc-self.resteBlanc)
        self.gapNoir = list(self.echiquier.setNoir - self.resteNoir)

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
        # while not self.partie_terminee():
        #     print(self.echiquier)
        #     print("\nAu tour du joueur {}".format(self.joueur_actif))
        #     source, cible = self.demander_positions()
        #     self.echiquier.deplacer(source, cible)
        #     self.joueur_suivant()
        #
        # print(self.echiquier)
        # print("\nPartie terminée! Le joueur {} a gagné".format(self.determiner_gagnant()))

    def position_mon_roi(self, couleur_joueur_actif):
        for position in self.echiquier.dictionnaire_pieces.keys():
            if isinstance(self.echiquier.dictionnaire_pieces[position], Roi) \
                    and self.echiquier.dictionnaire_pieces[position].couleur == couleur_joueur_actif:
                return position

    # Mélo
    def mon_roi_en_echec(self):
        position_roi = self.position_mon_roi(self.joueur_actif)
        if self.joueur_actif == 'blanc':
            autre_couleur = 'noir'
        else:
            autre_couleur = 'blanc'

        if self.partie_terminee():
            return False
        return self.echiquier.case_est_menacee_par(position_roi, autre_couleur)

    def sauvegarder_partie(self):
        """
        """
        with open(self.nom_fichier_sauvegarde, "wb") as f:
            pickle.dump(self.echiquier.dictionnaire_pieces, f)
        #TODO documenter la méthode

    def charger_partie(self):
        """
        """
        with open(self.nom_fichier_sauvegarde, "rb") as f:
            self.echiquier.dictionnaire_pieces = pickle.load(f)

        # self.echiquier.listeDesEchiquiers = []
        # self.echiquier.listeDesEchiquiers.append(dict({
        #     'a1': Tour('blanc'),
        #     'b1': Cavalier('blanc'),
        #     'c1': Fou('blanc'),
        #     'd1': Dame('blanc'),
        #     'e1': Roi('blanc'),
        #     'f1': Fou('blanc'),
        #     'g1': Cavalier('blanc'),
        #     'h1': Tour('blanc'),
        #     'a2': Pion('blanc'),
        #     'b2': Pion('blanc'),
        #     'c2': Pion('blanc'),
        #     'd2': Pion('blanc'),
        #     'e2': Pion('blanc'),
        #     'f2': Pion('blanc'),
        #     'g2': Pion('blanc'),
        #     'h2': Pion('blanc'),
        #     'a7': Pion('noir'),
        #     'b7': Pion('noir'),
        #     'c7': Pion('noir'),
        #     'd7': Pion('noir'),
        #     'e7': Pion('noir'),
        #     'f7': Pion('noir'),
        #     'g7': Pion('noir'),
        #     'h7': Pion('noir'),
        #     'a8': Tour('noir'),
        #     'b8': Cavalier('noir'),
        #     'c8': Fou('noir'),
        #     'd8': Dame('noir'),
        #     'e8': Roi('noir'),
        #     'f8': Fou('noir'),
        #     'g8': Cavalier('noir'),
        #     'h8': Tour('noir'),
        # }))
        # self.echiquier.listeDesEchiquiers.append(self.echiquier.dictionnaire_pieces)

        # self.echiquier.setBlanc = set()
        # self.echiquier.setNoir = set()
        # for i in self.echiquier.listeDesEchiquiers[0].values():
        #     if i.est_blanc():
        #         self.setBlanc.add(i)
        #     else:
        #         self.setNoir.add(i)
        # TODO documenter la méthode



# aa = ['(blanc)f2=>f4', '(noir)d7=>d5']
# print(', '.join(aa))
#
# dernierDeplacement = ("(" + piece.couleur + ")" + position_source + "=>" + position_cible])

if __name__ == '__main__':
    pass
