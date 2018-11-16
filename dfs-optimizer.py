from sys import path
import unittest
from dfs_optimizer import create_app, db
from dfs_optimizer.models import Player, User

app = create_app()
path.append(path[0]) # add top level folder to path


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Player': Player, 'User': User}


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
