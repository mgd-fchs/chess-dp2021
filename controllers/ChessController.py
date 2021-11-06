import sys
from flask import render_template, redirect, url_for, request, abort

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
    main()

# TODO
def store():
    ...

# TODO Change
# def show(userId):
#    ...

# def update(userId):
#    ...

# def delete(userId):
#    ...