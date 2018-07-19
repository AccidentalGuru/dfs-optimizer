from app import app, db
from app.models import Player, Team, User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Player': Player, 'Team': Team}
