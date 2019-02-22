#!/usr/bin/env python

__author__ = 'Tomas Novacik'


from board import PlayerType, Board


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
        self.player_move = None
        self.winning_player = None

    def _set_next_player_move(self):
        if self.player_move == PlayerType.CIRCLE:
            self.player_move = PlayerType.CROSS
        else:
            self.player_move = PlayerType.CIRCLE

    def start(self):
        self._board = Board()
        self.is_finished = False
        self.player_move = PlayerType.CIRCLE

    def move(self, move):
        if self.is_finished:
            raise GameAlreadyFinishedException()

        if move.player_type != self.player_move:
            raise InvalidPlayerMoveException()

        self._board.place_move(move)

        if self._board.is_winning_move(move):
            self.is_finished = True
            self.winning_player = move.player_type
        else:
            self._set_next_player_move()
# eof
