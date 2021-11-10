import sys
from flask import render_template, redirect, url_for, request, abort, jsonify, app, session
from flask import g

from controllers.Player import Player, ActiveState
from models.Chess import Chess

from flask_sqlalchemy import SQLAlchemy

from controllers.Game import Game

db = SQLAlchemy()


def init_new_game():
    game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    position = game.getFenString()
    color = game.getActivePlayer().getColor()
    state = game.gameState.name
    fullmove_number = game.fullmove_number
    if not db.engine.has_table('chessGame'):
        db.create_all()
    game_id = Chess.query.order_by(Chess.game_id.desc()).limit(1).all()[0].game_id + 1
    game_db = Chess(fen_String=position, game_id=game_id, active_state=1, move_id=0)
    db.session.add(game_db)
    db.session.commit()
    return game_id, position, color, state, fullmove_number


def load_the_game(game_id):
    if not db.engine.has_table('chessGame'):
        print("Cant load the game")
        return -1

    game_db = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.active_state == 1).limit(1).first()
    if game_db is None:
        game_db = db.session.query(Chess).filter(Chess.game_id == game_id).limit(1).first()
        game_db.active_state = 1
    game = Game(game_db.fen_String)
    db.session.commit()

    return game


def load_saved_game(game_id):
    if not db.engine.has_table('chessGame'):
        print("Cant load the game")
        return -1

    game_db = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.saved == 1).limit(1).first()
    if game_db is None:
        game_db = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.active_state == 1).limit(1).first()
    if game_db is None:
        db.session.commit()
        print("loading game error")
        return -1
    game = Game(game_db.fen_String)
    db.session.commit()

    position = game.getFenString()
    color = game.getActivePlayer().getColor()
    state = game.gameState.name
    fullmove_number = game.fullmove_number
    return game_id, position, color, state, fullmove_number


def save_game_by_id(game_id):
    game = load_the_game(game_id)

    # Set all other saved states from this game to 0
    prev_saved = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.saved == 1).all()
    for p in prev_saved:
        p.saved = 0
    db.session.commit()

    # save active state
    game_db = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.active_state == 1).limit(1).first()
    game_db.saved = 1
    db.session.commit()

    return game_id, game.getFenString(), game.getActivePlayer().getColor(), game.gameState.name, game.fullmove_number


def moving(game_id, moving_input):
    # load the game
    game = load_the_game(game_id)

    # do the move if its possible
    game.move(moving_input)

    # set other active game state to 0
    prev_state = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.active_state == 1).all()
    for p in prev_state:
        p.active_state = 0
        prev_move_id = p.move_id
    db.session.commit()

    move_id = prev_move_id + 1
    game_db = Chess(fen_String=game.getFenString(), game_id=game_id, active_state=1, move_id=move_id)
    db.session.add(game_db)
    db.session.commit()

    # delete all other states above move_id
    upcoming_moves = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.move_id > move_id)
    upcoming_moves.delete(synchronize_session=False)
    db.session.commit()

    return game_id, game.getFenString(), game.getActivePlayer().getColor(), game.gameState.name, game.fullmove_number


def redo_move(game_id):
    if not db.engine.has_table('chessGame'):
        print("Cant undo the game")
        return -1

    game_db = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.active_state == 1).limit(1).first()
    next_move_id = game_db.move_id + 1
    db.session.commit()

    next_move = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.move_id == next_move_id).limit(1).first()
    if next_move is None:
        print("That was the last move!")
        game = load_the_game(game_id)
        return game_id, game.getFenString(), game.getActivePlayer().getColor(), game.gameState.name, game.fullmove_number

    fen = next_move.fen_String
    db.session.commit()

    game_db = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.active_state == 1).limit(1).first()
    next_move.active_state = 1
    game_db.active_state = 0
    db.session.commit()

    game = Game(fen)

    return game_id, game.getFenString(), game.getActivePlayer().getColor(), game.gameState.name, game.fullmove_number


def undo_move(game_id):
    if not db.engine.has_table('chessGame'):
        print("Cant undo the game")
        return -1

    game_db = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.active_state == 1).limit(1).first()
    prev_move_id = game_db.move_id - 1
    game_db.active_state = 0
    db.session.commit()

    if prev_move_id < 0:
        print("Cant undo, that was the first step")
        game = load_the_game(game_id)
        return game_id, game.getFenString(), game.getActivePlayer().getColor(), game.gameState.name, game.fullmove_number

    db.session.commit()


    prev_move = db.session.query(Chess).filter(Chess.game_id == game_id, Chess.move_id == prev_move_id).limit(1).first()
    prev_move.active_state = 1
    fen = prev_move.fen_String
    db.session.commit()

    game = Game(fen)
    return game_id, game.getFenString(), game.getActivePlayer().getColor(), game.gameState.name, game.fullmove_number


def remove_game(game_id):
    games = db.session.query(Chess).filter(Chess.game_id == game_id)
    games.delete(synchronize_session=False)
    db.session.commit()


