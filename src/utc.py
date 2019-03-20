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

class GameFinished(Exception):

    def __init__(self, msg, winning_player, winning_move):
        super().__init__(msg)
        self.winning_player = winning_player
        self.winning_move = winning_move


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
        total_n = root_node.n

        actual_node = root_node

        top_nodes = []

        top_ucb1 = -math.inf
        top_node = actual_node

        while True:
            for n in actual_node.children:
                # TODO w/n could be computed in backprop phase
                ucb1 = n.w / n.n + math.sqrt(math.log(total_n) / n.n) * self.DEFAULT_C
                if ucb1 > top_ucb1:
                    top_ucb1 = ucb1
                    top_node = n

            top_nodes.append(top_node)

            if top_node.is_expandable:
                break
            else:
                actual_node = top_node

        return top_nodes

    def _playout(self, game: Game):
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
        # TODO what if node is not expandable
        # TODO what if winning move
        new_move = random.choice(game.available_moves)
        if game.player_move == PlayerType.CROSS:
            player_move = PlayerType.CIRCLE
        else:
            player_move = PlayerType.CROSS

        new_node = UTCNode(new_move, [], player_move)
        node.add_child(new_node)
        game.move(*new_move)
        # check if game is finished for either player
        # not checking edge cases in which there are not more moves
        if game.is_finished:
            raise GameFinished("Game is finished: {}(winning player)"
                               .format(game.winning_player),
                               game.winning_player,
                               new_move)

        if len(game.available_moves) <= 1:
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
        # TODO winning move found must stop the simulation
        iter_count = 0
        start_time = time.time()

        while not self._is_simulation_end(start_time, iter_count):
            nodes = self._selection(root_node)
            actual_game = game.clone() # TODO to much cloning
            for m in self._get_move_history(nodes[1:]):
                actual_game.move(*m)
            new_node = self._expand(nodes[-1], actual_game)
            # TODO raise exception with winning move
            new_game =self._playout(actual_game)
            self.backprop(nodes + [new_node], new_game)
            iter_count += 1

        logging.info("Simulation took:{}", time.time() - start_time)
        logging.info("Simulation took: {} iterations", iter_count)

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
        root_node = UTCNode(None, [], game.player_move)

        try:
            self._simulation(root_node, game.clone())
        except GameFinished as e:
            # TODO try again when other player wins
            return e.winning_move
        else:
            return self._get_winning_move(root_node)

    @staticmethod
    def backprop(nodes: UTCNodes, game):
        for node in nodes:
            node.n += 1

            if game.winning_player == node.player:
                node.w += 1
            elif game.winning_player is None:
                node.w += 0.5
            else:
                node.w -= 1

#eof