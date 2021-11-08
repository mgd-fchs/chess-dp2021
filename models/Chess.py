from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# Here comes what we want to save
class Chess(db.Model):
    __tablename__ = 'chessGame'

    moveID = db.Column(db.Integer, primary_key=True)
    fenString = db.Column(db.String)

    @property
    def serialize(self):
        return {
            'moveID': self.moveID,
            'FENString': self.fenString
        }

    def __init__(self, moveID, fenString):
        self.moveID = moveID
        self.fenString = fenString  

