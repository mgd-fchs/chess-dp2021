from alembic import op
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Here comes what we want to save
class Chess(db.Model):
    __tablename__ = 'chessGame'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fen_String = db.Column(db.String)
    game_id = db.Column(db.Integer)
    active_state = db.Column(db.Integer)
    saved = db.Column(db.Integer, default=0)

    @property
    def serialize(self):
        return {
            'id': self.moveID,
            'FENString': self.fen_String,
            'game_id': self.game_id,
            'active_state': self.active_state,
            'saved': self.saved
        }
