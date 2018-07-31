from flask import url_for
from werkzeug.security import check_password_hash, generate_password_hash
import base64
from datetime import datetime, timedelta
import os
from app import db


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'registered_on': self.registered_on.isoformat() + 'Z'
        }

        if include_email:
            data['email'] = self.email

        return data

    def from_dict(self, data):
         for field in ['username', 'email']:
             if field in data:
                 setattr(self, field, data[field])

         if 'password' in data:
             setattr(self, 'password_hash', generate_password_hash(data['password']))

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()

        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token

        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    position = db.Column(db.String(2), index=True) # qb, rb, wr, te, k
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    game_stats = db.relationship('Player_Game_Stats', backref='player', lazy='dynamic')

    def __repr__(self):
        return '<Player {} {}>'.format(self.position, self.name)


class Player_Game_Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, index=True)
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


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    abrev = db.Column(db.String(3), index=True, unique=True)
    players = db.relationship('Player', backref='team', lazy='dynamic')

    def __repr__(self):
        return '<Team {}>'.format(self.name)
