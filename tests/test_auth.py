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


if __name__=='__main__':
    unittest.main()
