from flask import request
from app.api import bp
from app.models import User


@bp.route('/login', methods=['POST'])
def login(username, password):
    pass


@bp.route('/logout')
def logout():
    pass


@bp.route('/register', methods=['POST'])
def register():
    pass
