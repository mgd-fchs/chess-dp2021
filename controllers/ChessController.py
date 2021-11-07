import sys
from flask import render_template, redirect, url_for, request, abort, jsonify, app, session
from flask import g

from controllers.Player import Player, ActiveState
from models.Chess import Chess

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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
    game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    position = game.getFenString()
    color = game.getActivePlayer().getColor()
    state = game.gameState.name
    return render_template('index.html', state=state, position=position, color=color)


# TODO
def start_new_game():
    print("starting...")
    game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    position = game.getFenString()
    color = game.getActivePlayer().getColor()
    state = game.gameState.name
    return render_template('index.html', state=state, position=position, color=color)


def load_game():
    print("loading...")
    position = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    color = "white"
    state = "end"
    return render_template('index.html', state=state, position=position, color=color)


def save_game():
    print("saving...")
    position = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    color = "white"
    state = "play"
    return render_template('index.html', state=state, position=position, color=color)


def undo():
    print("init undo...")
    position = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    color = "white"
    state = "play"
    return render_template('index.html', state=state, position=position, color=color)


def redo():
    print("init redo...")
    position = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    color = "white"
    state = "play"
    return render_template('index.html', state=state, position=position, color=color)


def show_history():
    print("showing history...")
    position = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    color = "white"
    state = "play"
    return render_template('index.html', state=state, position=position, color=color)


def move():
    print("moving...")
    game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move = request.form['movingInput']
    game.move(move)
    # simple testing calls, to be deleted
    #originSpot = newGame.board[0][1]
    #destinationSpot = newGame.board[0][2]

    # valid move
    #newGame.executeMove(originSpot, destinationSpot)
    position = game.getFenString()
    color = game.getActivePlayer().getColor()
    state = game.gameState.name
    return render_template('index.html', state=state, position=position, color=color)


def give_up():
    print("give up...")
    position = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    color = "white"
    state = "play"
    return render_template('index.html', state=state, position=position, color=color)

