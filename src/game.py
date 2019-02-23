#!/usr/bin/env python

__author__ = 'Tomas Novacik'


from board import PlayerType, Board, Move


class GameException(Exception):
    pass

class InvalidPlayerMoveException(GameException):
    pass

class GameAlreadyFinishedException(GameException):
    pass

class Game(object):
    """Governing game mechanism """

    def __init__(self):
        self._board = None
        self.is_finished = None
        self._player_move = None
        self.winning_player = None

    def _set_next_player_move(self):
        if self._player_move == PlayerType.CIRCLE:
            self._player_move = PlayerType.CROSS
        else:
            self._player_move = PlayerType.CIRCLE

    @property
    def player_move(self):
        return self._player_move

    @property
    def board(self):
        return self._board

    def start(self):
        self._board = Board()
        self.is_finished = False
        self._player_move = PlayerType.CIRCLE

    def move(self, x, y):
        if self.is_finished:
            raise GameAlreadyFinishedException()

        move = Move(x, y, self._player_move)

        self._board.place_move(move)

        if self._board.is_winning_move(move):
            self.is_finished = True
            self.winning_player = move.player_type
        else:
            self._set_next_player_move()
# eof
