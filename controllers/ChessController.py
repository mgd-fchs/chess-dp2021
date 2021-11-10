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


def init_new_game():
    game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    position = game.getFenString()
    color = game.getActivePlayer().getColor()
    state = game.gameState.name
    if not db.engine.has_table('chessGame'):
        db.create_all()
    game_id = Chess.query.order_by(Chess.game_id.desc()).limit(1).all()[0].game_id + 1
    game_db = Chess(fen_String=position, game_id=game_id, active_state=1)
    db.session.add(game_db)
    db.session.commit()
    return game_id, position, color, state


def load_the_game(game_id):
    if not db.engine.has_table('chessGame'):
        print("Cant load the game")
        return -1
    game_db = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.active_state == 1).limit(1).first()
    db.session.commit()
    print("load game state: id: " + str(game_db.game_id) + " state: " + str(game_db.active_state) + " fenstring: " + game_db.fen_String)
    game = Game(game_db.fen_String)

    return game


# TODO
def index():
    print("index...")
    db.session.rollback()
    game_id, position, color, state = init_new_game()
    return render_template('index.html', state=state, position=position, color=color, game_id=game_id)


# TODO
def start_new_game():
    print("starting...")
    game_id, position, color, state = init_new_game()
    return render_template('index.html', state=state, position=position, color=color, game_id=game_id)


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
    moving_input = request.form['movingInput']
    game_id = request.form['game_id']

    game = load_the_game(game_id)
    print("before move game state: id: " + str(game_id) + " fenstring: " + game.getFenString())

    game.move(moving_input)
    position = game.getFenString()
    color = game.getActivePlayer().getColor()
    state = game.gameState.name

    if not db.engine.has_table('chessGame'):
        db.create_all()

    # set other active game state to 0
    prev_state = db.session.query(Chess).filter(Chess.game_id == game_id and Chess.active_state == 1).first()
    prev_state.active_state = 0
    db.session.commit()

    # save active state
    game_db = Chess(fen_String=position, game_id=game_id, active_state=1)
    db.session.add(game_db)
    db.session.commit()
    print("save game state: id: " + str(game_db.game_id) + " state: " + str(game_db.active_state) + " fenstring: " + game_db.fen_String)

    return render_template('index.html', state=state, position=position, color=color, game_id=game_id)


def give_up():
    print("give up...")
    position = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    color = "white"
    state = "play"
    return render_template('index.html', state=state, position=position, color=color)
