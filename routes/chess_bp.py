from flask import Blueprint

from controllers.ChessController import index, start_new_game, load_game, save_game, undo, redo, show_history, move, give_up

chess_bp = Blueprint('chess_bp', __name__)

chess_bp.route('/', methods=['GET'])(index)
chess_bp.route('/new_game', methods=['POST'])(start_new_game)
chess_bp.route('/load_game', methods=['POST'])(load_game)
chess_bp.route('/save_game', methods=['POST'])(save_game)

chess_bp.route('/undo', methods=['POST'])(undo)
chess_bp.route('/redo', methods=['POST'])(redo)
chess_bp.route('/show_history', methods=['POST'])(show_history)

chess_bp.route('/move', methods=['POST'])(move)
chess_bp.route('/give_up', methods=['POST'])(give_up)

# add other routes
# chess_bp.route('/create', methods=['POST'])(store)
# chess_bp.route('/<int:user_id>', methods=['GET'])(show)
# chess_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# chess_bp.route('/<int:user_id>', methods=['DELETE'])(delete)