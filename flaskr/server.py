
from flask import Blueprint

from flaskr.serverController import temp, users, tokens, cleartokens, login, refresh, verify

bp = Blueprint('server', __name__, url_prefix='/')


bp.route('/temp', methods=['GET'])(temp)
bp.route('/users', methods=['GET'])(users)
bp.route('/tokens', methods=['GET'])(tokens)
bp.route('/cleartokens', methods=['GET'])(cleartokens)
bp.route('/login', methods=['POST'])(login)
bp.route('/refresh', methods=['POST'])(refresh)
bp.route('/verify', methods=['POST'])(verify)
