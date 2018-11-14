import os
from flask import make_response, jsonify, request
from app import db
from app.api import bp
from app.models import File, User
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['csv'])


def is_csv(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

        user_id = User.decode_auth_token(auth_token)
        filename = secure_filename(file.filename)
        print(filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))  # save to uploads folder
        file = File(
            filename=filename,
            user_id=user_id
        )

        db.session.add(file)
        db.session.commit()

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
