import datetime as dt

from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)

    def __init__(self, name):
        self.name = name
        self.created_at = dt.datetime.utcnow()

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Spot(db.Model):
    __tablename__ = 'spots'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    title = db.Column(db.String())

    sample_date = db.Column(db.String)
    wind_gust = db.Column(db.String())
    wind_speed = db.Column(db.String())
    air_pressure = db.Column(db.String())
    air_temp = db.Column(db.String())

    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = dt.datetime.utcnow()

    def update(
        self, title, date, wind_gust, wind_speed, air_pressure, air_temp, **kwargs
    ):
        self.updated_at = dt.datetime.utcnow()
        self.title = title
        self.sample_date = date
        self.wind_gust = wind_gust
        self.wind_speed = wind_speed
        self.air_pressure = air_pressure
        self.air_temp = air_temp

    def __repr__(self):
        return '<Spot {}>'.format(self.title)
