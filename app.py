from flask import Flask, render_template
from flask_migrate import Migrate

from models.Chess import db
from routes.chess_bp import chess_bp

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(chess_bp, url_prefix='/users')\

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()