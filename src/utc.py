#!/usr/bin/env python
import time
import math

from board import Move

__author__ = 'Tomas Novacik'

import random
import logging

from typing import List, Optional
from game import PlayerType, Game
from board import BoardCoord

UTCNodes = List["UTCNode"]
Moves = List[Move]


class WinningMoveFound(Exception):
    def __init__(self, winning_move: BoardCoord):
        self.winning_move = winning_move


class SearchFinished(Exception):
    pass


class UTCNode:

    def __init__(self, move: Optional[BoardCoord], children: UTCNodes,
                 player: PlayerType):
        self.move = move
        self.children = children
        self.player = player
        self.n = 0
        self.w = 0
        self._is_expandable = True

    def add_child(self, child) -> None:
        self.children.append(child)

    @property
    def is_expandable(self) -> bool:
        return self._is_expandable

    @is_expandable.setter
    def is_expandable(self, value: bool):
        self._is_expandable = value


class UTC:

    DEFAULT_C = 1.4
    DEFAULT_PLAYOUT_MAX_DEPTH = 100 # maximum search limit
    DEFAULT_TIME_LIMIT = 10 # secs

    def __init__(self, time_limit: float = DEFAULT_TIME_LIMIT,
                 max_depth: int = DEFAULT_PLAYOUT_MAX_DEPTH,
                 iteration_limit: Optional[int] = None):
        """
        In case iteration limit is specified time_limit is ignored.

        :param time_limit: search timi limit in seconds
        :type time_limit: int
        :param max_depth: maximum depth of playout
        :type max_depth: int
        :param iteration_limit: maximum iteration limit - overrides time limit
        :type iteration_limit: int
        """
        self._time_limit = time_limit
        self._max_depth = max_depth
        self._iteration_limit = iteration_limit

        # for inspection during tests only
        self.root_node = None

    def _get_move_history(self, nodes: UTCNodes) -> List[BoardCoord]:
        return [n.move for n in nodes]

    def _selection(self, root_node: UTCNode) -> UTCNodes:
        logging.debug("Selecting new node to expand.")
        total_n = root_node.n

        actual_node = root_node

        top_nodes = [actual_node]

        top_node = actual_node

        previous_node = None

        while True:
            if actual_node.is_expandable:
                break

            # local minimum encountered - end the search
            if actual_node == previous_node:
                raise SearchFinished()

            previous_node = actual_node

            top_ucb1 = -math.inf
            for n in actual_node.children:
                # TODO w/n could be computed in backprop phase
                ucb1 = n.w / n.n + math.sqrt(math.log(total_n) / n.n) * self.DEFAULT_C
                if ucb1 > top_ucb1:
                    top_ucb1 = ucb1
                    top_node = n

            top_nodes.append(top_node)

            actual_node = top_node

        return top_nodes

    def _playout(self, game: Game):
        logging.debug("Starting playout game.")
        moves_played = 0

        new_game = game.clone()

        while moves_played < self._max_depth:
            if new_game.is_finished:
                break
            x, y = random.choice(new_game.board.available_moves)
            new_game.move(x, y)

            moves_played += 1

        return new_game

    def _expand(self, node: UTCNode, game: Game):
        logging.debug("Expanding node.")

        assert game.available_moves, "There should be always avail. moves"
        assert not game.is_finished, "Game should not be finished"

        used_moves = set([c.move for c in node.children])

        aval_moves = set(game.available_moves) - used_moves

        new_move = random.choice(list(aval_moves))

        new_node = UTCNode(new_move, [], game.player_move)

        game.move(*new_move)
        node.add_child(new_node)

        if game.is_finished:
            new_node.is_expandable = False

        if len(aval_moves) == 1:
            node.is_expandable = False

        return new_node

    def _is_simulation_end(self, start_time: float, iter_count: int):
        """
        End simulation of time/iter limit was reached depending on initial setup
        """
        if self._iteration_limit is not None:
            return iter_count >= self._iteration_limit
        return time.time() - start_time >= self._time_limit

    def _simulation(self, root_node: UTCNode, game: Game):
        iter_count = 0
        start_time = time.time()

        while not self._is_simulation_end(start_time, iter_count):
            nodes = self._selection(root_node)
            actual_game = game.clone() # TODO to much cloning
            for m in self._get_move_history(nodes[1:]):
                actual_game.move(*m)

            new_node = self._expand(nodes[-1], actual_game)

            # check if it is forced win
            if (len(nodes) == 1 and
                actual_game.is_finished and
                game.player_move == actual_game.winning_player):
                raise WinningMoveFound(new_node.move)

            new_game =self._playout(actual_game)
            self.backprop(nodes + [new_node], new_game)
            iter_count += 1
            logging.debug("Finish iteration num. {}".format(iter_count))

        logging.debug("Simulation finished.")
        logging.debug("It took:{}".format(time.time() - start_time))
        logging.debug("It took: {} iterations".format(iter_count))

    def _get_winning_move(self, root_node: UTCNode) -> BoardCoord:
        """
        Possibilities in literature:
        1. Max child - highest reward
        2. Robust child - most visited
        3. Max-Robust child - highest reward && highest visit count
        4. Secure child - maximizes lower confidence bound

        Option 2. is implemented
        """
        nodes = root_node.children
        top_node = nodes[0]

        for node in nodes[1:]:
            if top_node.n < node.n:
                top_node = node

        return top_node.move

    def get_move(self, game: Game) -> BoardCoord:
        if game.player_move == PlayerType.CIRCLE:
            player_move = PlayerType.CROSS
        else:
            player_move = PlayerType.CIRCLE

        root_node = UTCNode(None, [], player_move)

        try:
            self._simulation(root_node, game.clone())
        except WinningMoveFound as e:
            return e.winning_move
        except SearchFinished as e:
            logging.debug("Searching finished.")

        return self._get_winning_move(root_node)

    @staticmethod
    def backprop(nodes: UTCNodes, game):
        logging.debug("Backpropagating stats.")
        for node in nodes:
            node.n += 1

            if game.winning_player == node.player:
                node.w += 1
            elif game.winning_player is None:
                node.w += 0.5
            else:
                node.w -= 1

#eof