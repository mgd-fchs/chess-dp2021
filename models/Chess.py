from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Here comes what we want to save
class Chess(db.Model):
    __tablename__ = 'chessGame'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer)
    move_id = db.Column(db.Integer)
    fen_String = db.Column(db.String)
    active_state = db.Column(db.Integer)
    saved = db.Column(db.Integer, default=0)

    @property
    def serialize(self):
        return {
            'id': self.moveID,
            'game_id': self.game_id,
            'move_id': self.move_id,
            'FENString': self.fen_String,
            'active_state': self.active_state,
            'saved': self.saved
        }
