#!/usr/bin/env python

import unittest2
import random

from utc import UTC
from game import Game
from game import PlayerType

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

# eof
