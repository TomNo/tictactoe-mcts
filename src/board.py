#!/usr/bin/env python

import enum
import pprint
from typing import Tuple, Optional, List, NamedTuple

__author__ = 'Tomas Novacik'

BoardCoord = Tuple[int, int]
BoardCoordList = List[BoardCoord]

class InvalidMoveException(Exception):
    pass


class PlayerType(enum.Enum):
    """Player type identification"""
    CROSS = 'X'
    CIRCLE = 'O'

class Move:
    """Move representation"""
    def __init__(self, x, y, player_type):
        self.x = x
        self.y = y
        self.player_type = player_type

    def __str__(self):
        return "Move(x = {}, y = {}, player_type = {})"\
            .format(self.x, self.y, self.player_type)


BoardSpec = NamedTuple("BoardSpec",
                       [("width", int), ("height", int), ("winning_count", int)])

class Board:
    """Board representation"""

    # constants
    DEFAULT_WIDTH = 10
    DEFAULT_HEIGHT = 10
    DEFAULT_WINNING_MOVE_COUNT = 5
    EMPTY_FIELD_VALUE = '_'
    # private methods

    def __init__(self, spec:Optional[BoardSpec] = None,
                 board: List[List[str]] = None,
                 available_moves: Optional[BoardCoordList] = None):
        self.spec = spec
        if spec:
            self.width = spec.width
            self.height = spec.height
            self.winning_move_count = spec.winning_count
        else:
            self.width = self.DEFAULT_WIDTH
            self.height = self.DEFAULT_HEIGHT
            self.winning_move_count = self.DEFAULT_WINNING_MOVE_COUNT

        self._board = board or [[self.EMPTY_FIELD_VALUE] * self.width for _ in range(self.height)]
        self.available_moves = available_moves or [(x, y) for x in range(self.width) for y in range(self.height)]

    def __str__(self):
        return "Board(width = {}, height = {})\n{}"\
            .format(self.width, self.height,
                    "\n".join([pprint.pformat(row) for row in self._board]))

    # public methods

    def place_move(self, move: Move):
        if move.x >= self.width or move.x < 0\
                or move.y < 0 or move.y >= self.height:
            raise InvalidMoveException(
                "Attempting move:{} beyond the board boarders: {}, {}"
                    .format(move, move.x, move.y))

        if self._board[move.x][move.y] != self.EMPTY_FIELD_VALUE:
            raise InvalidMoveException(
                "Attempting move {} but field is already occupied by: {}"
                    .format(move, self._board[move.x][move.y]))

        self._board[move.x][move.y] = move.player_type.value
        self.available_moves.remove((move.x, move.y))

    @property
    def board(self) -> []:
        return self._board

    def get_field(self, x:int, y:int) -> PlayerType:
        return PlayerType(self.board[x][y])

    def _is_partially_winning(self, x: int, y: int, move: Move) -> bool:
        return self.board[x][y] == move.player_type.value

    def _is_horizontal_winning_move(self, move: Move) -> bool:
        left_border = max(0, move.x - self.winning_move_count)
        right_border = min(self.width, move.x + self.winning_move_count)

        succ_count = 0

        for i in range(left_border, right_border):
            if self._is_partially_winning(i, move.y, move):
                succ_count += 1
            else:
                succ_count = 0

            if succ_count == self.winning_move_count:
                return True

        return False

    def _is_vertical_winning_move(self, move: Move) -> bool:
        top_border = min(self.height, move.y + self.winning_move_count)
        down_border = max(move.y - self.height, 0)

        succ_count = 0

        for i in range(down_border, top_border):
            if self._is_partially_winning(move.x, i, move):
                succ_count += 1
            else:
                succ_count = 0

            if succ_count == self.winning_move_count:
                return True

        return False

    def _is_diagonal_winning_move(self, move: Move) -> bool:
        max_x_shift_left = max(0, move.x - self.winning_move_count + 1)
        max_y_shift_down = max(0, move.y - self.winning_move_count + 1)
        max_x_shift_right = min(self.width - 1, move.x + self.winning_move_count - 1)
        max_y_shift_top = min(self.height - 1, move.y + self.winning_move_count - 1)

        max_left_down = min(move.x - max_x_shift_left, move.y - max_y_shift_down)
        max_right_top = min(max_x_shift_right - move.x, max_y_shift_top - move.y)
        max_left_top = min(move.x - max_x_shift_left, max_y_shift_top - move.y)
        max_right_down = min(max_x_shift_right - move.x, move.y - max_y_shift_down)

        x_cords = range(move.x - max_left_down, move.x + max_right_top + 1)
        y_cords = range(move.y - max_left_down, move.y + max_right_top + 1)

        succ_count = 0

        for x, y in zip(x_cords, y_cords):
            if self._is_partially_winning(x, y, move):
                succ_count += 1
            else:
                succ_count = 0

            if succ_count == self.winning_move_count:
                return True

        x_cords = range(move.x - max_left_top, move.x + max_right_down + 1)
        y_cords = range(move.y + max_left_top, move.y - max_right_down - 1, -1)

        succ_count = 0

        for x, y in zip(x_cords, y_cords):
            if self._is_partially_winning(x, y, move):
                succ_count += 1
            else:
                succ_count = 0

            if succ_count == self.winning_move_count:
                return True

        return False

    def is_winning_move(self, move: Move) -> bool:
        # TODO not checking move borders issue?
        return self._is_horizontal_winning_move(move) or\
               self._is_vertical_winning_move(move) or\
                self._is_diagonal_winning_move(move)

    def clone(self):
        new_board = None if self.board is None else [row[:] for row in self.board]
        new_available_moves = self.available_moves.copy()

        return Board(self.spec, new_board, new_available_moves)

# eof