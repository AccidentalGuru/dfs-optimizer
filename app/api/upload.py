from flask import make_response, jsonify, request
from app.api import bp


@bp.route('/upload', methods=['POST'])
def upload():
    post_data = request.get_json()
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
        responseObject = {
            'status': 'success',
            'data': {
                'file': '/projections.csv'
            }
        }

        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }

        return make_response(jsonify(responseObject)), 401
