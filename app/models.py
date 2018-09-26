from flask import current_app, url_for
import jwt
from datetime import datetime, timedelta
import os
from app import bcrypt, db


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

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
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
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    position = db.Column(db.String(2), index=True) # qb, rb, wr, te, k
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    game_stats = db.relationship('Player_Game_Stats', backref='player', lazy='dynamic')

    def __repr__(self):
        return '<Player {} {}>'.format(self.position, self.name)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    abrev = db.Column(db.String(3), index=True, unique=True)
    players = db.relationship('Player', backref='team', lazy='dynamic')

    def __repr__(self):
        return '<Team {}>'.format(self.name)


class Player_Game_Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    season = db.Column(db.Integer)
    week = db.Column(db.Integer)
    dropbacks = db.Column(db.Integer)
    attempts = db.Column(db.Integer)
    aimed = db.Column(db.Integer)
    completions = db.Column(db.Integer)
    passing_yds = db.Column(db.Integer)
    passing_tds = db.Column(db.Integer)
    passing_adot = db.Column(db.Float)  # average depth of target as passer
    interceptions = db.Column(db.Integer)
    sacks = db.Column(db.Integer)
    completion_percentage = db.Column(db.Float)
    adjusted_completion_percentage = db.Column(db.Float)
    carries = db.Column(db.Integer)
    rushing_yards = db.Column(db.Integer)
    rushing_tds = db.Column(db.Integer)
    rushing_fumbles = db.Column(db.Integer)
    yds_per_carry = db.Column(db.Float)
    yds_after_contact = db.Column(db.Float)  # per carry
    tackles_avoided = db.Column(db.Integer)
    tackles_avoided_per_attempt = db.Column(db.Float)
    targets = db.Column(db.Integer)
    receptions = db.Column(db.Integer)
    receiving_yds = db.Column(db.Integer)
    receiving_tds = db.Column(db.Integer)
    receiving_fumbles = db.Column(db.Integer)
    receiving_adot = db.Column(db.Float)  # average depth of target as receiver
    drops = db.Column(db.Integer)
    catch_percentage = db.Column(db.Float)
    yds_per_reception = db.Column(db.Float)
    yds_per_target = db.Column(db.Float)
    receiving_yds_after_catch = db.Column(db.Float)  # per catch
    fantasy_points_standard = db.Column(db.Integer)
    fantasy_points_ppr = db.Column(db.Integer)


    def stats_from_dict(self, data):
        pass
