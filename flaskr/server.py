
from flask import Blueprint

from flaskr.serverController import temp, users, tokens, cleartokens, login, refresh, verify

bp = Blueprint('server', __name__, url_prefix='/')

bp.route('/login', methods=['POST'])(login)
bp.route('/refresh', methods=['POST'])(refresh)
bp.route('/verify', methods=['POST'])(verify)
