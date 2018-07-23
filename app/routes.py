from flask import jsonify, make_response, render_template, request, session
from sqlalchemy import or_
from app import app, db
from app.models import User


@app.route('/api/login', methods=['POST'])
def login():
    post_data = request.get_json()

    try:
        user = User.query.filter_by(username=post_data.get('username')).first()

        if user and user.check_password(post_data.get('password')):
            auth_token = user.encode_auth_token(user.id)

            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Succesfully logged in.',
                    'auth_token': auth_token.decode()
                }

                return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Invalid username or password.'
            }

            return make_response(jsonify(response_object)), 404
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Try again'
        }

        return make_response(jsonify(response_object)), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        resp = User.decode_auth_token(auth_token)

        if not isinstance(resp, str):
            blacklist_token = BlacklistToken(token=auth_token)

            try:
                db.session.add(blacklist_token)
                db.session.commit()
                response_object = {
                    'status': 'success',
                    'message': 'Succesfully logged out.'
                }

                return make_response(jsonify(response_object)), 200
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': e
                }

                return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'status': 'fail',
                'message': resp
            }

            return make_response(jsonify(response_object)), 403
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403


@app.route('/api/register', methods=['POST'])
def register():
    post_data = request.get_json()
    user = User.query.filter(or_(User.username==post_data.get('username'), User.email==post_data.get('email'))).first()

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
            response_object = {
                'status': 'success',
                'message': 'Succesfully registered.',
                'auth_token': auth_token.decode()
            }

            return make_response(jsonify(response_object)), 201
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }

            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.'
        }

        return make_response(jsonify(response_object)), 202


@app.route('/api/user', methods=['GET'])
def user():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(' ')[1]
        except IndexError:
            response_object = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }

            return make_response(jsonify(response_object)), 401
    else:
        auth_token = ''

    if auth_token:
        resp = User.decode_auth_token(auth_token)

        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            response_object = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'registered_on': user.registered_on
                }
            }

            return make_response(jsonify(response_object)), 200

        response_object = {
            'status': 'fail',
            'message': resp
        }

        return make_response(jsonify(response_object)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }

        return make_response(jsonify(responseObject)), 401


# Routes should be added above this so they take precedence over catch all
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')
