from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path):
    # catch_all catches all non-api routes so routing can be done on frontend
    return render_template('index.html')
