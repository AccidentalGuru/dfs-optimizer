from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    position = db.Column(db.String(2), index=True) # qb, rb, wr, te, k
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<Player {} {}>'.format(self.position, self.name)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    abrev = db.Column(db.String(3), index=True, unique=True)

    def __repr__(self):
        return '<Team {}>'.format(self.name)
