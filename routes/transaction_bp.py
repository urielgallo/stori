from flask import Blueprint
from controllers.transactionsController import insert, show, update, delete, read_data, process

transaction_bp = Blueprint('transaction_bp', __name__)

#transaction_bp.route('/', methods=['GET'])(index)
transaction_bp.route('/insert', methods=['GET'])(insert)
transaction_bp.route('/show', methods=['GET'])(show)
transaction_bp.route('/update', methods=['GET'])(update)
transaction_bp.route('/delete', methods=['GET'])(delete)
transaction_bp.route('/read_data', methods=['GET'])(read_data)
transaction_bp.route('/process', methods=['GET'])(process)
#transaction_bp.route('/<int:user_id>', methods=['GET'])(show)
#transaction_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
#transaction_bp.route('/<int:user_id>', methods=['DELETE'])(delete)