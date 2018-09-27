from flask import make_response, request, jsonify
from app import db
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
    post_data = request.get_json()
    user = User.query.filter_by(username=post_data.get('username')).first()
    if not user:
        user = User.query.filter_by(email=post_data.get('email')).first()

    if not user:
        try:
            user = User(
                username=post_data.get('username'),
                email=post_data.get('email'),
                password=post_data.get('password')
            )

            db.session.add(user)
            db.session.commit()
            auth_token = user.encode_auth_token(user.id)

            responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
            }

            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }

            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }

        return make_response(jsonify(responseObject)), 202
