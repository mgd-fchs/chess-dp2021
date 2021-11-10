from flask_sqlalchemy import SQLAlchemy
from models.Chess import db

from models.Chess import Chess

db = SQLAlchemy()


def test_new_chess():
    """
    GIVEN a Chess model
    WHEN a new Chess is created
    THEN check the fen_String, game_id, active_state and saved fields are defined correctly
    """

    chess = Chess(fen_String='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', game_id=1, active_state=1)

    assert chess.fen_String == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    assert chess.game_id == 1
    assert chess.active_state == 1
    assert chess.saved is None
