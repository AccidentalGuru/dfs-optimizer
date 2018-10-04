import json
import unittest
from app import db
from app.models import User
from base import BaseTestCase


class TestAuthBluePrint(BaseTestCase):
    def test_registration(self):
        response = self.client.post(
            '/api/register',
            data=json.dumps(dict(username='test', email='test@test.com', password='test')),
            content_type='application/json'
        )

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

        response = self.client.post(
            '/api/register',
            data=json.dumps(dict(username='test', email='test@test.com', password='test')),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'User already exists. Please Log in.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 202)

    def test_login_with_registered_user(self):
        resp_register = self.client.post(
            '/api/register',
            data=json.dumps(dict(username='test', email='test@test.com', password='test')),
            content_type='application/json'
        )

        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['message'] == 'Successfully registered.')
        self.assertTrue(data_register['auth_token'])
        self.assertEqual(resp_register.status_code, 201)

        response = self.client.post(
            '/api/login',
            data=json.dumps(dict(username='test', password='test')),
            content_type='application/json'
        )

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_non_registered_user(self):
        response = self.client.post(
            '/api/login',
            data=json.dumps(dict(username='test', password='test')),
            content_type='application/json'
        )

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'User does not exist.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_user_status(self):
        resp_register = self.client.post(
            '/api/register',
            data=json.dumps(dict(username='test', email='test@test.com', password='test')),
            content_type='application/json'
        )

        response = self.client.get(
            '/api/status',
            headers=dict(
                Authorization='Bearer ' + json.loads(resp_register.data.decode())['auth_token']
            )
        )

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['data'] is not None)
        self.assertTrue(data['data']['email'] == 'test@test.com')
        self.assertTrue(data['data']['admin'] is 'true' or 'false')
        self.assertEqual(response.status_code, 200)


if __name__=='__main__':
    unittest.main()
