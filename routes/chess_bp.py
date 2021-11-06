from flask import Blueprint

from controllers.ChessController import index, start_new_game # import other methods store, show, update, delete

chess_bp = Blueprint('chess_bp', __name__)

chess_bp.route('/', methods=['GET'])(index)
chess_bp.route('/new_game', methods=['POST'])(start_new_game)

# add other routes
# chess_bp.route('/create', methods=['POST'])(store)
# chess_bp.route('/<int:user_id>', methods=['GET'])(show)
# chess_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# chess_bp.route('/<int:user_id>', methods=['DELETE'])(delete)