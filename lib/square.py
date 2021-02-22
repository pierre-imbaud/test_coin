#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""contains inFile class, instances resulting of file
   read at the start of the script
   The script ability to read many files induces data
   (plateau, but equally "vide", "obstacle", "plein") instanciated many times:
   might as well live in a class instance
"""

import collections
import sys

# coordonnées d'un point sur le plateau. les x sont les abcisses,
# ils numérotent les colonnes,
# les y numérotent les lignes, 0 est la premiere ligne, 1 la seconde...
Point = collections.namedtuple('Point', ['x', 'y'])


class inFile():
    """ Instances will contain data read from file, and data processed
    methods will implement the algorithm
    """

    def __init__(self, input):
        """ create instance from input file
        """
        self.fname = input
        if input == '-':
            self.read_content(sys.stdin)
        else:
            with open(input, 'r') as inf:
                self.read_content(inf)

    def read_content(self, inf):
        """ read content from input flow
        """
        spl = spec_line = inf.readline().strip()
        del spec_line
        # fix! might strip leading spaces, if eg vide char is space
        if len(spl) < 4:
            raise ValueError('premiere ligne %s pas assez longue' % spl)
        nb_lines, self.vide, self.obstacle, self.plein = \
            spl[:-3], spl[-3], spl[-2], spl[-1]
        try:
            self.nb_lines = int(nb_lines)
        except ValueError:
            raise ValueError('%s: int attendu' % nb_lines)
        # lire le plateau: tuple de tuples
        self.plateau = tuple([tuple(x.strip())
                              for x in inf][:self.nb_lines])
        self.recouche()
        self.nb_cols = self.check()

    def recouche(self):
        """ recalcule l'attribut plateau_couche
            mis dans une methode pour aider les TU, qui patchent plateau
        """
        self.plateau_couche = tuple(zip(*self.plateau))

    def check(self):
        """teste le plateau apres lecture.
        retourne le nombre de colonnes
        """

        if len(self.plateau) != self.nb_lines:
            raise ValueError(
                f"{self.fname}: {self.nb_lines} attendues, " +
                f"{len(self.plateau)} lignes")

        authorized_chars = set((self.vide, self.obstacle))

        nb_cols = len(self.plateau[0])
        for line in self.plateau:
            if len(line) != nb_cols:
                raise ValueError(f"{self.fname}: lignes inegales")
            chars = set(line)
            if not chars <= authorized_chars:
                raise ValueError(f"{self.fname}: caracteres non attendus")
        return nb_cols

    def value(self, point):
        """valeur du datum en ce point
        """
        return self.plateau[point.y][point.x]

    def barre_h(self, point, lg):
        """ retourne la barre horizontale partant de point,
        dirigee à droite, de longueur lg
        """
        return self.plateau[point.y][point.x:point.x + lg]

    def barre_v(self, point, lg):
        """ retourne la barre verticale partant de point,
        dirigee vers le bas, de longueur lg
        """
        return self.plateau_couche[point.x][point.y:point.y + lg]

    def barre_sh(self, point, lg):
        """ comme barre_h, mais string (pour debug)
        """
        return ''.join(self.barre_h(point, lg))

    def barre_sv(self, point, lg):
        """ comme barre_v, mais string (pour debug)
        """
        return ''.join(self.barre_v(point, lg))

    def scan_carre(self, coin):
        """scan du plus grand carre depuis un coin

        version incrementale
        return la dimension du carré. 0 indique que le coin est un obstacle
        """

        """max_value: taille max possible sans obstacle:
        on atteint les limites du plateau
        """
        max_value = min(self.nb_lines - coin.y, self.nb_cols - coin.x)

        obstacle = self.obstacle
        if self.value(coin) == obstacle:
            return 0

        for taille in range(0, max_value):
            diagonale = self.plateau[coin.y + taille][coin.x + taille]
            if diagonale == obstacle:
                return taille
            coin_bas = Point(coin.x, coin.y + taille)
            if obstacle in self.barre_h(coin_bas, taille):
                return taille

            coin_droit = Point(coin.x + taille, coin.y)
            if obstacle in self.barre_v(coin_droit, taille):
                return taille
        try:
            return taille + 1
        except NameError:
            return 0            # on était au bord, pas passé dans le for.

    def scan_brutal(self):
        """ invoque scan_carre sur tous les points du plateau

        stocke les plus grands trouves (sans garder les petits)
        puis choisit et stocke le plus grand dans result
        """

        found = []              # plus grands carres trouves
        max_size = 0

        for x in range(self.nb_cols):
            for y in range(self.nb_lines):
                coin = Point(x, y)
                taille = self.scan_carre(coin)
                if taille > max_size:
                    found = [(coin, taille)]
                    max_size = taille
                elif taille == max_size:
                    found.append((coin, taille))

        if not found:
            self.result = None  # possible s'il n'y a que des obstacles
            return
        assert found
        if len(found) == 1:
            self.result = found[0]
            return
        # plusieurs resultats. Trier par point le plus petit possible:
        found.sort()
        self.result = found[0]
        return

    def fill_plateau(self, check=False):
        """ invoquer quand self.result est disponible: compute alors
            et retourne le plateau avec le carre rempli
            si check: verifie que la zone ecrite est bien vide
        """
        point, taille = self.result
        ligne_pleine = [self.plein] * taille
        lilist = [list(line) for line in self.plateau]
        for y in range(point.y, point.y + taille):
            if check:
                assert set(lilist[y][point.x:point.x + taille]) == {'.'}
            lilist[y][point.x:point.x + taille] = ligne_pleine

        return lilist

    def print_plateau(self, plateau=None):
        """ print le plateau fourni, ou si none
        le plateau self.plateau

        plateau = None sert en debug
        """

        if not plateau:
            plateau = self.plateau
        for line in plateau:
            print(''.join(line))


def main():
    """ pour debug
    """
    instance = inFile('example_file')
    instance.scan_brutal()
    plateau = instance.fill_plateau()
    instance.print_plateau(plateau)
    return instance
