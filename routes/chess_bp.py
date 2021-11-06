from flask import Blueprint

from controllers.ChessController import index # import other methods store, show, update, delete

chess_bp = Blueprint('user_bp', __name__)

chess_bp.route('/', methods=['GET'])(index)
# add other routes
# chess_bp.route('/create', methods=['POST'])(store)
# chess_bp.route('/<int:user_id>', methods=['GET'])(show)
# chess_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# chess_bp.route('/<int:user_id>', methods=['DELETE'])(delete)