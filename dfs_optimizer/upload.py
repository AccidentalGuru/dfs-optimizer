import csv
import os
from flask import Blueprint, make_response, jsonify, request
from werkzeug.utils import secure_filename
from dfs_optimizer import db
from dfs_optimizer.models import File, Player, User

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['csv'])
bp = Blueprint('upload', __name__)


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
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)  # save to uploads folder
        file = File(
            filename=filename,
            user_id=user_id
        )

        db.session.add(file)
        db.session.commit()
        read_file_data(file_path)
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


def read_file_data(file_path):
    with open(file_path, encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            rank = int(row['Rnk'])
            name = row['Name']
            team = row['Team']
            pos = row['Pos']
            opp = row['Game']
            points = float(row['Pts'])
            salary = int(row['Sal'][1:]) if row['Sal'] != 'N/A' else 0

            player = Player(
                rank=rank,
                name=name,
                team=team,
                position=pos,
                opponent=opp,
                projection=points,
                salary=salary
            )

            db.session.add(player)
        db.session.commit()
