import io
import json
import unittest
from base import BaseTestCase, login_user, register_user


class TestUpload(BaseTestCase):
    def test_upload(self):
        register_user(self, 'test', 'test@test.com', 'test')
        login_resp = login_user(self, 'test', 'test')
        auth_token = json.loads(login_resp.data.decode())['auth_token']
        data = dict(file=(io.BytesIO(b'test'), 'test_file.csv'))

        response = self.client.post(
            '/api/upload',
            headers=dict(
                Authorization='Bearer ' + auth_token
            ),
            data=data,
            content_type='multipart/form-data'
        )

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'File uploaded Successfully.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_upload_no_file(self):
        register_user(self, 'test', 'test@test.com', 'test')
        login_resp = login_user(self, 'test', 'test')
        auth_token = json.loads(login_resp.data.decode())['auth_token']
        data = None

        response = self.client.post(
            '/api/upload',
            headers=dict(
                Authorization='Bearer ' + auth_token
            ),
            data=data,
            content_type='multipart/form-data'
        )

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Request does not contain a file param.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_upload_invalid_file_type(self):
        register_user(self, 'test', 'test@test.com', 'test')
        login_resp = login_user(self, 'test', 'test')
        auth_token = json.loads(login_resp.data.decode())['auth_token']
        data = dict(file=(io.BytesIO(b'test'), 'test_file.jpg'))

        response = self.client.post(
            '/api/upload',
            headers=dict(
                Authorization='Bearer ' + auth_token
            ),
            data=data,
            content_type='multipart/form-data'
        )

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'File is not a csv.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main(verbosity=2)
