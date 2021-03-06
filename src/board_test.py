#!/usr/bin/env python

import unittest2

from board import PlayerType, Move, Board, InvalidMoveException, BoardSpec

__author__ = 'Tomas Novacik'


class SmallBoardTest(unittest2.TestCase):
    def setUp(self):
        board_spec = BoardSpec(3, 3, 3)
        self.test_board = Board(board_spec)

    def test_diagonal_win(self):
        self.test_board.place_move(Move(2, 0, PlayerType.CIRCLE))
        self.test_board.place_move(Move(1, 1, PlayerType.CIRCLE))

        win_move = Move(0, 2, PlayerType.CIRCLE)
        self.test_board.place_move(win_move)

        assert self.test_board.is_winning_move(win_move) == True


class BoardTest(unittest2.TestCase):

    def setUp(self):
        board_spec = BoardSpec(10, 10, 5)
        self.test_board = Board(board_spec)

    def test_placing_circle_move(self):
        self.test_board.place_move(Move(0, 0, PlayerType.CIRCLE))

        assert(self.test_board.get_field(0, 0) == PlayerType.CIRCLE)

    def test_placing_cross_move(self):
        self.test_board.place_move(Move(0, 0, PlayerType.CROSS))

        assert(self.test_board.get_field(0, 0) == PlayerType.CROSS)

    def test_placing_invalid_cross_move(self):
        self.test_board.place_move(Move(0, 0, PlayerType.CROSS))

        with self.assertRaises(InvalidMoveException):
            self.test_board.place_move(Move(0, 0, PlayerType.CROSS))

    def test_placing_invalid_circle_move(self):
        self.test_board.place_move(Move(0, 0, PlayerType.CIRCLE))

        with self.assertRaises(InvalidMoveException):
            self.test_board.place_move(Move(0, 0, PlayerType.CIRCLE))

    def test_placing_move_outside_board(self):
        test_move = Move(self.test_board.width, self.test_board.height,
                               PlayerType.CIRCLE)

        with self.assertRaises(InvalidMoveException):
            self.test_board.place_move(test_move)

    def test_is_winning_move_vertical(self):
        test_moves = [Move(0, i, PlayerType.CIRCLE) for i in range(4)]
        for move in test_moves:
            self.test_board.place_move(move)

        winning_move = Move(0, 4, PlayerType.CIRCLE)
        self.test_board.place_move(winning_move)

        self.assertTrue(self.test_board.is_winning_move(winning_move))

    def test_is_winning_move_horizontal(self):
        test_moves = [Move(i, 0, PlayerType.CIRCLE) for i in range(4)]
        for move in test_moves:
            self.test_board.place_move(move)

        winning_move = Move(4, 0, PlayerType.CIRCLE)
        self.test_board.place_move(winning_move)

        self.assertTrue(self.test_board.is_winning_move(winning_move))

    def test_is_winning_move_diagonal_trivial(self):
        test_moves = [Move(i, i, PlayerType.CIRCLE) for i in range(4)]
        for move in test_moves:
            self.test_board.place_move(move)

        winning_move = Move(4, 4, PlayerType.CIRCLE)
        self.test_board.place_move(winning_move)

        self.assertTrue(self.test_board.is_winning_move(winning_move))

    def test_is_winning_move_diagonal_complex(self):
        test_moves = [Move(x, y, PlayerType.CIRCLE) for x, y in [(5, 5), (7, 3), (8, 2), (9, 1)]]
        for move in test_moves:
            self.test_board.place_move(move)

        winning_move = Move(6, 4, PlayerType.CIRCLE)
        self.test_board.place_move(winning_move)

        self.assertTrue(self.test_board.is_winning_move(winning_move))

    def test_is_winning_move_horizontal_inter(self):
        test_moves = [Move(i, 0, PlayerType.CIRCLE) for i in range(2)]
        for move in test_moves:
            self.test_board.place_move(move)

        test_moves = [Move(i, 0, PlayerType.CIRCLE) for i in range(3, 5)]
        for move in test_moves:
            self.test_board.place_move(move)

        winning_move = Move(2, 0, PlayerType.CIRCLE)
        self.test_board.place_move(winning_move)

        self.assertTrue(self.test_board.is_winning_move(winning_move))

    def test_is_winning_move_vertical_inter(self):
        test_moves = [Move(0, i, PlayerType.CIRCLE) for i in range(2)]
        for move in test_moves:
            self.test_board.place_move(move)

        test_moves = [Move(0, i, PlayerType.CIRCLE) for i in range(3, 5)]
        for move in test_moves:
            self.test_board.place_move(move)

        winning_move = Move(0, 2, PlayerType.CIRCLE)
        self.test_board.place_move(winning_move)

        self.assertTrue(self.test_board.is_winning_move(winning_move))

    def test_is_winning_move_diagonal_inter(self):
        test_moves = [Move(i, i, PlayerType.CIRCLE) for i in range(2)]
        for move in test_moves:
            self.test_board.place_move(move)

        test_moves = [Move(i, i, PlayerType.CIRCLE) for i in range(3, 5)]
        for move in test_moves:
            self.test_board.place_move(move)

        winning_move = Move(2, 2, PlayerType.CIRCLE)
        self.test_board.place_move(winning_move)

        self.assertTrue(self.test_board.is_winning_move(winning_move))

    def test_is_not_winning_move(self):
        not_winning_move = Move(2, 2, PlayerType.CIRCLE)

        self.test_board.place_move(not_winning_move)

        self.assertFalse(self.test_board.is_winning_move(not_winning_move))

    def tearDown(self):
        self.test_board = None
# eof
