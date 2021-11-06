from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# Here comes what we want to save
class Chess(db.Model):
    __tablename__ = 'chessGame'

    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String)
    # age = db.Column(db.String(120))
    # address = db.Column(db.String(120))

    @property
    def serialize(self):
        return {
            'id': self.id,
            # 'name': self.name,
            # 'city': self.city,
            # 'state': self.state,
            # 'address': self.address
        }

