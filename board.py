#!/usr/bin/env python

import enum

__author__ = 'Tomas Novacik'


class InvalidMoveException(Exception):
    pass

class PlayerType(enum.Enum):
    CROSS = 1
    CIRCLE = 2

class Move:

    def __init__(self, x, y, player_type):
        pass

class Board:
    """Board representation"""
    # constants
    DEFAULT_WIDTH = 10
    DEFAULT_HEIGHT = 10
    DEFAULT_WINNING_MOVE_COUNT = 5
    # private methods

    def __init__(self, width = DEFAULT_WIDTH, height = DEFAULT_HEIGHT,
                 winning_move_count = DEFAULT_WINNING_MOVE_COUNT):
        self.width = width
        self.height = height
        self.winning_move_count = winning_move_count
        self._board = [[0.0] * width] * height

    def place_move(self, move):
        pass

    @property
    def board(self):
        return self._board

    def is_winning_move(self, move):
        pass

    # public methods

    # protected methods

    # class methods

    # static methods

# eof
