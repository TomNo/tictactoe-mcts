#!/usr/bin/env python

import unittest2
import random
from board import BoardSpec
from utc import UTC
from game import Game

__author__ = 'Tomas Novacik'


class UtcTest(unittest2.TestCase):

    def setUp(self):
        random.seed(1)

    def test_get_first_move(self):
        game = Game()
        game.start()

        utc = UTC(iteration_limit=100)
        move = utc.get_move(game)

        assert move == (1, 7)

    def test_finding_last_move(self):
        board_spec = BoardSpec(3, 3, 3)
        game = Game(board_spec = board_spec)
        game.start()

        game.move(1, 0)
        game.move(0, 0)

        game.move(2, 1)
        game.move(1, 1)

        game.move(0, 1)
        game.move(2, 0)

        game.move(1, 2)

        utc = UTC(iteration_limit=100)
        move = utc.get_move(game)

        assert move == (2, 2)

    def test_ucb_computation(self):
        board_spec = BoardSpec(3, 3, 3)
        game = Game(board_spec = board_spec)
        game.start()

        utc = UTC(iteration_limit=20)
        move = utc.get_move(game)

        assert move == (0, 1)

# eof
