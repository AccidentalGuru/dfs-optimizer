import json
import unittest
from base import BaseTestCase, login_user, register_user


class TestUpload(BaseTestCase):
    def test_upload(self):
        resp_register = register_user(self, 'test', 'test@test.com', 'test')
        response = login_user(self, 'test', 'test')

    def test_upload_no_file(self):
        pass
        
    def test_upload_invalid_file_type(self):
        pass
