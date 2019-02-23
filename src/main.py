#!/usr/bin/env python

__author__ = 'Tomas Novacik'

from game import Game


def start_game():
    game = Game()

    game.start()

    while True:
        move = input("Type new move for player {}:".format(game.player_move))

        try:
            x, y = move.split(",")
            game.move(int(x), int(y))
            print("Game status:")
            print(game.board)
        except Exception as err:
            print("Oops error:")
            print(err)
            print("Try again")
            continue

        if game.is_finished:
            print("Player {} won.".format(game.winning_player))
            break


def main():
    start_game()


if __name__ == "__main__":
    main()