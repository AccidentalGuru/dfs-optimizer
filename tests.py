from datetime import datetime, timedelta
import sqlalchemy
import unittest
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_missing_param(self):
        with self.assertRaises(TypeError):
            u = User(username='jrojas', password='apple')

        with self.assertRaises(TypeError):
            u = User(username='jrojas', email='email@email.com')

        with self.assertRaises(TypeError):
            u = User(email='email@email.com', password='pass')

    def test_password_hashing(self):
        u = User(username='jmrojas', email='email@email.com', password='cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
        
    def test_user_uniqueness(self):
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            u = User(username='jmrojas', email='email@email.com', password='cat')
            u2 = User(username='jmrojas', email='email2@email.com', password='cat')
            db.session.add(u)
            db.session.add(u2)
            db.session.commit()

        db.session.rollback()

        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            u = User(username='jmrojas', email='email@email.com', password='cat')
            u2 = User(username='jmrojas2', email='email@email.com', password='cat')
            db.session.add(u)
            db.session.add(u2)
            db.session.commit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
