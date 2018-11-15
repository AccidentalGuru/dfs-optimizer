import json
import unittest
from base import BaseTestCase, get_user_status, login_user, logout_user, register_user
from dfs_optimizer import db
from dfs_optimizer.models import BlacklistToken, User


class TestAuthBluePrint(BaseTestCase):
    def test_registration(self):
        response = register_user(self, 'test', email='test@test.com', password='test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_registration_with_already_registered_user(self):
        user = User(
            username='test',
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()

        response = register_user(self, 'test', 'test@test.com', 'test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'User already exists. Please Log in.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 202)

    def test_login_with_registered_user(self):
        resp_register = register_user(self, 'test', 'test@test.com', 'test')
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['message'] == 'Successfully registered.')
        self.assertTrue(data_register['auth_token'])
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, 201)

        response = login_user(self, 'test', 'test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_non_registered_user(self):
        response = login_user(self, 'test', 'test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'User does not exist.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_user_status(self):
        resp_register = register_user(self, 'test', 'test@test.com', 'test')
        response = get_user_status(self, json.loads(resp_register.data.decode())['auth_token'])
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['data'] is not None)
        self.assertTrue(data['data']['email'] == 'test@test.com')
        self.assertTrue(data['data']['admin'] is 'true' or 'false')
        self.assertEqual(response.status_code, 200)

    def test_valid_logout(self):
        resp_register = register_user(self, 'test', 'test@test.com', 'test')
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['message'] == 'Successfully registered.')
        self.assertTrue(data_register['auth_token'])
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, 201)

        resp_login = login_user(self, 'test', 'test')
        data_login = json.loads(resp_login.data.decode())
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['auth_token'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)

        response = logout_user(self, json.loads(resp_register.data.decode())['auth_token'])
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged out.')
        self.assertEqual(response.status_code, 200)

    def test_valid_blacklisted_token_logout(self):
        resp_register = register_user(self, 'test', 'test@test.com', 'test')
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['message'] == 'Successfully registered.')
        self.assertTrue(data_register['auth_token'])
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, 201)

        resp_login = login_user(self, 'test', 'test')
        data_login = json.loads(resp_login.data.decode())
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['auth_token'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)

        blacklist_token = BlacklistToken(
            token=json.loads(resp_login.data.decode())['auth_token'])
        db.session.add(blacklist_token)
        db.session.commit()

        response = logout_user(self, json.loads(resp_login.data.decode())['auth_token'])
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
        self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_user(self):
        resp_register = register_user(self, 'test', 'test@test.com', 'test')
        blacklist_token = BlacklistToken(
            token=json.loads(resp_register.data.decode())['auth_token'])
        db.session.add(blacklist_token)
        db.session.commit()

        response = get_user_status(self, json.loads(resp_register.data.decode())['auth_token'])
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
        self.assertEqual(response.status_code, 401)


if __name__=='__main__':
    unittest.main()
