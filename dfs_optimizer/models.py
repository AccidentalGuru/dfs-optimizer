from datetime import datetime, timedelta
from flask import current_app
import jwt
from dfs_optimizer import bcrypt, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password,
            current_app.config['BCRYPT_LOG_ROUNDS']
        ).decode()
        self.registered_on = datetime.utcnow()
        self.admin = admin

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=1800),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, current_app.config['SECRET_KEY'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)

            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.utcnow()

    def __repr__(self):
        return '<Token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()

        if res:
            return True
        else:
            return False


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rank = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    team = db.Column(db.String(3), nullable=False)
    position = db.Column(db.String(2), nullable=False)
    opponent = db.Column(db.String(4), nullable=False)
    projection = db.Column(db.Float, nullable=False)
    salary = db.Column(db.Integer, nullable=False)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
