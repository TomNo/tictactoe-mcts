#!/usr/bin/env python

__author__ = 'Tomas Novacik'


import unittest2

from game import Game
from board import Board, PlayerType, Move


class GameTest(unittest2.TestCase):

    def test_winning_move(self):
        game = Game()
        game.start()

        # set winning status to board
        board = Board()
        [board.place_move(Move(0, i, PlayerType.CIRCLE)) for i in range(4)]
        winning_move = 0, 4

        game._board = board
        game.move(*winning_move)

        self.assertTrue(game.is_finished)

    def test_clone(self):
        game = Game()
        game.clone()
# eof
