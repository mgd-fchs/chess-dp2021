import sys
from flask import render_template, redirect, url_for, request, abort, jsonify, app, session
from flask import g

from controllers.Player import Player, ActiveState
from models.Chess import Chess

from flask_sqlalchemy import SQLAlchemy

from controllers.Game import Game
from controllers.Gamplay import init_new_game, load_the_game, load_saved_game, save_game_by_id, moving, redo_move, undo_move
db = SQLAlchemy()

# TODO
def index():
    print("index...")
    db.session.rollback()
    game_id, position, color, state, fullmove_number = init_new_game()
    fullmove_number = 1
    return render_template('index.html', state=state, position=position, color=color, game_id=game_id,
                           fullmove_number=fullmove_number)


# TODO
def start_new_game():
    print("starting...")
    game_id, position, color, state, fullmove_number = init_new_game()
    return render_template('index.html', state=state, position=position, color=color, game_id=game_id,
                           fullmove_number=fullmove_number)


def load_game():
    print("loading...")
    game_id = request.form['game_id']

    game_id, position, color, state, fullmove_number = load_saved_game(game_id)

    return render_template('index.html', state=state, position=position,
                           color=color, game_id=game_id, fullmove_number=fullmove_number)


def save_game():
    print("saving...")
    game_id = request.form['game_id']

    game_id, position, color, state, fullmove_number = save_game_by_id(game_id)

    return render_template('index.html', state=state, position=position, color=color, game_id=game_id,
                           fullmove_number=fullmove_number)


def undo():
    print("init undo...")
    game_id = request.form['game_id']

    game_id, position, color, state, fullmove_number = undo_move(game_id)

    return render_template('index.html', state=state, position=position, color=color, game_id=game_id,
                           fullmove_number=fullmove_number)


def redo():
    print("init redo...")
    game_id = request.form['game_id']

    game_id, position, color, state, fullmove_number = redo_move(game_id)

    return render_template('index.html', state=state, position=position, color=color, game_id=game_id,
                           fullmove_number=fullmove_number)


def move():
    print("moving...")
    moving_input = request.form['movingInput']
    game_id = request.form['game_id']

    game_id, position, color, state, fullmove_number = moving(game_id, moving_input)

    return render_template('index.html', state=state, position=position, color=color, game_id=game_id,
                           fullmove_number=fullmove_number)


def give_up():
    print("give up...")
    position = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    color = "white"
    state = "play"
    return render_template('index.html', state=state, position=position, color=color)
