from flask import make_response, jsonify, request
from app.api import bp


def is_csv(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@bp.route('/upload', methods=['POST'])
def upload():
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
        if 'file' not in request.files:
            responseObject = {
                'status': 'fail',
                'message': 'Request does not contain a file param.'
            }

            return make_response(jsonify(responseObject)), 400

        file = request.files['file']

        if file.filename == '':
            responseObject = {
                'status': 'fail',
                'message': 'No file selected.'
            }

            return make_response(jsonify(responseObject)), 400

        if not is_csv(file.filename):
            responseObject = {
                'status': 'fail',
                'message': 'File is not a csv.'
            }

            return make_response(jsonify(responseObject)), 400

        # save_file(file)
        # read_data(file.read())

        responseObject = {
            'status': 'success',
            'message': 'File uploaded Successfully.'
        }

        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }

        return make_response(jsonify(responseObject)), 401
