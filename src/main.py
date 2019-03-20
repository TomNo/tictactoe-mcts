#!/usr/bin/env python
from board import BoardSpec

__author__ = 'Tomas Novacik'

import argparse

from game import Game
from utc import UTC


def start_game(with_bot):
    utc = None
    if with_bot:
        utc = UTC()

    game = Game(board_spec=BoardSpec(3, 3, 3))

    game.start()

    move_num = 0

    while True:
        if not with_bot or move_num % 2 == 0:
            move = input("Type new move for player {}:".format(game.player_move))

            try:
                x, y = move.split(",")
            except Exception as err:
                print("Oops error:")
                print(err)
                print("Try again")
                continue
        else:
            x, y = utc.get_move(game)

        game.move(int(x), int(y))

        print("Game status:")
        print(game.board)

        if game.is_finished:
            print("Player {} won.".format(game.winning_player))
            break

        move_num += 1

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-w", "--with-bot", help="Player 2 will be bot",
                    action="store_true", default = False)

    args = parser.parse_args()
    start_game(args.with_bot)

if __name__ == "__main__":
    main()