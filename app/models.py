import datetime as dt

from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)

    def __init__(self, name):
        self.name = name
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<User {}>'.format(self.name)
