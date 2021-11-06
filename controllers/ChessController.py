import sys
from flask import render_template, redirect, url_for, request, abort, jsonify

from models.Chess import Chess

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# imports
from controllers.Game import Game

def main():
    newGame = Game()

    # simple testing calls, to be deleted
    originSpot = newGame.board[0][1]
    destinationSpot = newGame.board[0][2]

    # valid move
    newGame.executeMove(originSpot, destinationSpot)
    """ expected output: 
        This is a valid move!
        Moving piece x to coordinates
    """

    # valid move but wrong player
    newGame.executeMove(destinationSpot, newGame.board[0][3])
    """ expected output: 
        This is a valid move!
        Cannot make move, it's not your turn
    """

    # correct player but invalid move
    newGame.executeMove(newGame.board[0][6], newGame.board[0][7])
    """ expected output: 
        Please select a valid move!
    """


# TODO
def index():
    print("index...")
    # main()
    print("starting...")
    position = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    color = "white"
    state = "play"
    return render_template('index.html', state=state, position=position, color=color)


# TODO
def start_new_game():
    print("starting...")
    position = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    color = "white"
    state = "play"
    return render_template('index.html', state=state, position=position, color=color)



# TODO Change
# def show(userId):
#    ...

# def update(userId):
#    ...

# def delete(userId):
#    ...