import json
import os
import unittest
from config import Config
from dfs_optimizer import create_app, db

basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL') or \
        'sqlite:///' + os.path.join(basedir, 'test.db')


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()  # test client to make requests
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


def register_user(self, username, email, password):
    return self.client.post(
        '/api/register',
        data=json.dumps(dict(
            username=username,
            email=email,
            password=password)),
        content_type='application/json'
    )


def login_user(self, username, password):
    return self.client.post(
        '/api/login',
        data=json.dumps(dict(
            username=username,
            password=password)),
        content_type='application/json'
    )


def logout_user(self, token):
    return self.client.post(
        '/api/logout',
        headers=dict(
            Authorization='Bearer ' + token
        )
    )


def get_user_status(self, token):
    return self.client.get(
        '/api/status',
        headers=dict(
            Authorization='Bearer ' + token
        )
    )
