from sys import path
import unittest
from app import create_app, db
from app.models import User

app = create_app()
path.append(path[0]) # add top level folder to path


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Player': Player, 'Team': Team}


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
