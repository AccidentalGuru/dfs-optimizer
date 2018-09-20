from flask import render_template
from app.main import bp


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path):
    # catch_all catches all non-api routes so routing can be done on frontend
    return render_template('index.html')
