#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" pytest compliant test file
"""

import pytest
import unittest
from unittest import mock

import square as mut            # module under test


cut = mut.inFile            # class under test

base_sample = """4.ox
.......
.o.....
......o
ooooooo
"""

not_an_int = base_sample.replace('4', '4t')
with_unexp_char  = base_sample.replace('.o.', 'vo.')
unequal = base_sample.replace('ooooooo', 'oooooo')
sample = mock.mock_open(read_data = base_sample)

@pytest.fixture
def virgin10():
    """ a 10x10 plateau with no obstacle
    """
    iut = cut('tests/10nobs')
    return iut

@pytest.fixture
def spotted10():
    """ a 10x10 plateau with no obstacle
    """
    iut = cut('tests/10nobs')
    plateau = list([list(x) for x in iut.plateau])
    plateau[4][4] = iut.obstacle
    iut.plateau = plateau
    iut.recouche()
    return iut

@pytest.fixture
def squarobs():
    """ a 10x10 plateau with a 3x3 obstacle centered
    """
    iut = virgin10()
    plateau = list([list(x) for x in iut.plateau])
    obstacle3 = [obstacle] * 3
    for index in 3,4,5:
        plateau[index][3:6] = obstacle3
        assert len(plateau[index]) == 10
    iut.plateau = plateau
    iut.recouche()
    return iut

class Test_init:
    """ test init
    """
    cut = mut.inFile            # class under test


    def test_nominal(self):
        iut = cut('tests/10nobs')
        plateau = iut.plateau
        plateau_couche = iut.plateau_couche
        assert type(plateau) == tuple
        for line in plateau:
            assert type(line) == tuple
            for char in line:
                assert type(char) == str
                assert len(char) == 1

        assert type(plateau_couche) == tuple
        for line in plateau_couche:
            assert type(line) == tuple
            for char in line:
                assert type(char) == str
                assert len(char) == 1



    def test_mocked_open(self):
        with mock.patch('builtins.open', sample) as fname:
            iut = cut(fname)
            assert set(iut.plateau[-1]) == {'o'}


    def test_init_fails(self):
        with mock.patch('builtins.open',
                        mock.mock_open(read_data = with_unexp_char)) as fname:
            with pytest.raises(ValueError) as excinfo:
                iut = cut(fname)

        with mock.patch('builtins.open',
                        mock.mock_open(read_data = unequal)) as fname:
            with pytest.raises(ValueError) as excinfo:
                iut = cut(fname)

        with mock.patch('builtins.open',
                        mock.mock_open(read_data = not_an_int)) as fname:
            with pytest.raises(ValueError) as excinfo:
                iut = cut(fname)

class Test_barre:

    def test_barre_h(self):
        expected = {
            (0,0,7): '.' * 7,
            (0,0,6): '.' * 6,
            (1,0,6): '.' * 6,
            (1,1,6): 'o.....'
            }

        with mock.patch('builtins.open', sample) as fname:
            iut = cut(fname)
            for k in expected.keys():
                x, y, lg = k
                pt = mut.Point(x, y)
                barre = ''.join(iut.barre_h(pt, lg))
                assert barre == expected[k]


    def test_barre_v(self):
        expected = {
            (0,0,4): '...o',
            (0,1,3): '..o',
            }

        with mock.patch('builtins.open', sample) as fname:
            iut = cut(fname)
            for k in expected.keys():
                x, y, lg = k
                pt = mut.Point(x, y)
                barre = ''.join(iut.barre_v(pt, lg))
                assert barre == expected[k]

class Test_fill_plateau:

    def check(self, plateau, iut):
        """verifie la taille du carre plein du plateau
        """
        coin, taille = iut.result
        filled = [x for x in plateau  if iut.plein * taille in ''.join(x)]
        assert len(filled) == taille
        for line in filled:
            assert line.index(iut.plein) == coin.x
            assert line.count(iut.plein) == taille

    def test_fill(self):
        with mock.patch('builtins.open', sample) as fname:
            iut = cut(fname)
            iut.result = mut.Point(0,0), 1
            rez = iut.fill_plateau()
            self.check(rez, iut)

            iut.result = mut.Point(0,0), 4
            rez = iut.fill_plateau()
            self.check(rez, iut)

            iut.result = mut.Point(1,1), 3
            rez = iut.fill_plateau()
            self.check(rez, iut)


class Test_Scan_Carre:

    """ test scan_carre method
    """

    def test_nominal10(self, virgin10):

        iut = virgin10

        coin = mut.Point(0,0)
        taille = iut.scan_carre(coin)
        assert taille == 10

        coin = mut.Point(1,1)
        taille = iut.scan_carre(coin)
        assert taille == 9

        coin = mut.Point(8, 8)
        taille = iut.scan_carre(coin)
        assert taille == 2

        coin = mut.Point(9,9)
        taille = iut.scan_carre(coin)
        assert taille == 1

        # sans rester sur la diagonale:
        coin = mut.Point(1,4)
        taille = iut.scan_carre(coin)
        assert taille == 6

        coin = mut.Point(4,1)
        taille = iut.scan_carre(coin)
        assert taille == 6


    def test_nominal_obs(self, spotted10):
        """ add an obstacle in the middle
        """
        iut = spotted10

        coin = mut.Point(0,0)
        taille = iut.scan_carre(coin)
        assert taille == 4

        coin = mut.Point(0,3)
        taille = iut.scan_carre(coin)
        assert taille == 4

        coin = mut.Point(3,0)
        taille = iut.scan_carre(coin)
        assert taille == 4
