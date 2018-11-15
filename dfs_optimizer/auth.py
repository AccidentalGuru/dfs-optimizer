from flask import Blueprint, make_response, jsonify, request
from dfs_optimizer import bcrypt, db
from dfs_optimizer.models import BlacklistToken, User

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    post_data = request.get_json()

    try:
        if post_data.get('username'):
            user = User.query.filter_by(username=post_data.get('username')).first()
        else:
            user = User.query.filter_by(email=post_data.get('email')).first()

        if user and bcrypt.check_password_hash(user.password, post_data.get('password')):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }

                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }

            return make_response(jsonify(responseObject)), 404
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }

        return make_response(jsonify(responseObject)), 500


@bp.route('/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token = auth_header.split(' ')[1]
    else:
        auth_token = ''

    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):

            blacklist_token = BlacklistToken(token=auth_token)

            try:
                db.session.add(blacklist_token)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }

                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': e
                }

                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }

            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403



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
                'message': e
            }

            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }

        return make_response(jsonify(responseObject)), 202


@bp.route('/status', methods=['GET'])
def status():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        try:
            auth_token = auth_header.split(' ')[1]
        except IndexError:
            responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }

            return make_response(jsonify(responseObject)), 401
    else:
        auth_token = ''

    if auth_token:
        resp = User.decode_auth_token(auth_token)

        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': user.registered_on
                }
            }

            return make_response(jsonify(responseObject)), 200

        responseObject = {
            'status': 'fail',
            'message': resp
        }

        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }

        return make_response(jsonify(responseObject)), 401
