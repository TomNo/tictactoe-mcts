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

    def __init__(self, board = None, is_finished = None, player_move = None,
                 winning_player = None):
        self._board = board
        self.is_finished = is_finished
        self._player_move = player_move
        self.winning_player = winning_player

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
        elif len(self._board.available_moves) == 0:
            self.is_finished = True # draw
            self.winning_player = None
        else:
            self._set_next_player_move()

    @property
    def available_moves(self):
        return self.board.available_moves

    def clone(self):
        return Game(self._board.clone(), self.is_finished, self._player_move,
                    self.winning_player)
# eof
