from flask import Flask, render_template, jsonify
from flask_migrate import Migrate

from models.Chess import db
from routes.chess_bp import chess_bp

# Controller split into three parts:
# Initialization
app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

# Routing is outsources with blueprint
app.register_blueprint(chess_bp, url_prefix='/')

# Execution
if __name__ == '__main__':
    app.debug = True
    app.run()
