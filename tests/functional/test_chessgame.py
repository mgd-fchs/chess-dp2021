import pytest
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from routes.chess_bp import chess_bp

from controllers.Gamplay import *

db = SQLAlchemy()


@pytest.fixture(scope="session")
def app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config['TESTING'] = True
    app.register_blueprint(chess_bp, url_prefix='/')

    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)
    return app


def test_init_chess(app):
    with app.app_context():
        game_id, position, color, state, fullmove_number = init_new_game()
        assert(position == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        remove_game(game_id)


def test_init_move(app):
    with app.app_context():
        game_id, position, color, state, fullmove_number = init_new_game()
        game_id_2, position_2, color_2, state_2, fullmove_number_2 = moving(game_id, "Pa2 Pa3")
        assert(game_id == game_id_2)
        assert(position != position_2)
        assert(position_2 == "rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b KQkq - 0 1")
        assert (color == "white")
        assert (color_2 == "black")
        assert (fullmove_number_2 == fullmove_number)
        remove_game(game_id)



def test_init_move_save_move(app):
    with app.app_context():
        game_id, position, color, state, fullmove_number = init_new_game()
        game_id_2, position_2, color_2, state_2, fullmove_number_2 = moving(game_id, "Pa2 Pa3")
        game_id_3, position_3, color_3, state_3, fullmove_number_3 = save_game_by_id(game_id)
        game_id_4, position_4, color_4, state_4, fullmove_number_4 = moving(game_id, "pa7 pa6")
        assert(position_4 == "rnbqkbnr/1ppppppp/p7/8/8/P7/1PPPPPPP/RNBQKBNR w KQkq - 0 2")
        assert(position_2 == position_3)
        remove_game(game_id)


def test_load_move_load(app):
    with app.app_context():
        game_id, position, color, state, fullmove_number = init_new_game()
        game_id_2, position_2, color_2, state_2, fullmove_number_2 = moving(game_id, "Pa2 Pa3")
        game_id_3, position_3, color_3, state_3, fullmove_number_3 = save_game_by_id(game_id)
        game_id_4, position_4, color_4, state_4, fullmove_number_4 = moving(game_id, "pa7 pa6")

        game_id_5, position_5, color_5, state_5, fullmove_number_5 = load_saved_game(game_id)
        game_id_6, position_6, color_6, state_6, fullmove_number_6 = moving(game_id, "Pb2 Pb3")
        game_id_7, position_7, color_7, state_7, fullmove_number_7 = load_saved_game(game_id)

        assert(position_5 == "rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b KQkq - 0 1")
        assert(position_5 == position_7)
        assert(position_6 != position_7)
        remove_game(game_id)



def test_load_move_undo_redo(app):
    with app.app_context():
        game_id, position, color, state, fullmove_number = init_new_game()
        game_id_2, position_2, color_2, state_2, fullmove_number_2 = moving(game_id, "Pa2 Pa3")
        game_id_3, position_3, color_3, state_3, fullmove_number_3 = moving(game_id, "pa7 pa6")
        game_id_4, position_4, color_4, state_4, fullmove_number_4 = undo_move(game_id)

        assert(position_4 == "rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b KQkq - 0 1")
        assert(position_2 == position_4)
        assert(position_2 != position_3)

        game_id_5, position_5, color_5, state_5, fullmove_number_5 = redo_move(game_id)
        assert (position_5 == "rnbqkbnr/1ppppppp/p7/8/8/P7/1PPPPPPP/RNBQKBNR w KQkq - 0 2")
        assert (position_3 == position_5)
        assert (position_5 != position_4)
        remove_game(game_id)


