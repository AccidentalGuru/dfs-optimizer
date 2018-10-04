import unittest
from app import db
from app.models import User
from base import BaseTestCase
from config import Config


class TestUserModel(BaseTestCase):
    def test_encode_auth_token(self):
        user = User(username='test', email='test@test.com', password='test')
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(username='test', email='test@test.com', password='test')
        db.session.add(user)
        db.session.commit()
        auth_token= user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode('utf-8')) == 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
