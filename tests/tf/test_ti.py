#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" pytest compliant functional test file
    fix: logger les résultats et les étapes, sur stderr, pour permettre
    la surveillance du process, et/ou un rapport de test
"""

import pytest
import subprocess as sp

params = [(5, 5, 1), (11, 11, 1), (8, 4, 2), (113, 83, 5)]


@pytest.fixture(scope="module", params=params)
def map(request):
    """ generate a map file based on params
    """

    command = ['./scripts/map_gen.py'] + [str(x) for x in request.param]
    process = sp.Popen(command, stdout=sp.PIPE)
    return process.stdout.read().decode()


def map1(params):
    """ almost same as map, with a single set of params.
    some factoring needed here, no time to think it out.
    """

    command = ['./scripts/map_gen.py'] + [str(x) for x in params]
    process = sp.Popen(command, stdout=sp.PIPE)
    return process.stdout.read().decode()


def check_result(result):
    """ tester que result comporte bien un carre

    tester que le carre repond bien au probleme
    est un peu hors de portee de l'exercice
    """
    lines = result.split()
    xlines = [l for l in lines if 'x' in l]
    size = len(xlines)
    chunk = 'x' * size
    toomuch = 'x' * (size + 1)
    for xline in xlines:
        assert chunk in xline
        assert toomuch not in xline


class Test_Nominal:
    def test_one(self, map):
        # write the map file:
        with open('current_test_map_file', 'w') as cmf:
            cmf.write(map)
        command = ['./scripts/find_square', 'current_test_map_file']
        process = sp.Popen(command, stdout=sp.PIPE)
        result = process.stdout.read().decode()
        assert result
        with open('current_test_result', 'w') as f:
            f.write(result)
        check_result(result)

    def test_many(self):
        # write the map files:
        fnames = []
        for index, param in enumerate(params):
            fname = f'current_test_map_file{index}'
            fnames.append(fname)
            map = map1(param)
            with open(fname, 'w') as cmf:
                cmf.write(map)
        command = ['./scripts/find_square'] + fnames
        process = sp.Popen(command, stdout=sp.PIPE)
        result = process.stdout.read().decode()
        assert result
        with open('many_test_result', 'w') as f:
            f.write(result)

    def test_from_stdin(self, map):
        "as test_one, but reading file from stdin"

        command = ['./scripts/find_square', "-"]
        process = sp.Popen(command, stdin=sp.PIPE, stdout=sp.PIPE)
        process.stdin.write(bytes(map, "utf-8"))
        result = process.stdout.read().decode()
        assert 22
        assert result
        with open('many_test_result', 'w') as f:
            f.write(result)        


    def test_from_stdin(self, map):
        "as test_one, but reading file from stdin"

        command = ['./scripts/find_square', "-"]
        process = sp.Popen(command, stdin=sp.PIPE, stdout=sp.PIPE)
        process.stdin.write(bytes(map, "utf-8"))
        process.stdin.close()
        result = process.stdout.read().decode()
        assert result
        with open('many_test_result', 'w') as f:
            f.write(result)        
