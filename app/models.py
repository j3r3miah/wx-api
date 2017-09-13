from datetime import datetime, timedelta

from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)

    def __init__(self, name):
        self.name = name
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Spot(db.Model):
    __tablename__ = 'spots'

    FETCH_INTERVAL = timedelta(minutes=5)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    wind_gust = db.Column(db.String())
    wind_speed = db.Column(db.String())
    air_pressure = db.Column(db.String())
    air_temp = db.Column(db.String())
    sample_date = db.Column(db.String)

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    touched_at = db.Column(db.DateTime)

    def __init__(self):
        self.created_at = datetime.utcnow()
        self.touched_at = datetime.utcnow()

    def should_refresh(self):
        """ If spot has been touched within the update interval """
        return self.touched_at > datetime.utcnow() - Spot.FETCH_INTERVAL

    def needs_refresh(self):
        """ If spot hasn't been updated since update interval """
        # TODO could use sample_date and knowledge of update period
        return not self.updated_at or (
            self.updated_at < datetime.utcnow() - Spot.FETCH_INTERVAL
        )

    def touch(self):
        self.touched_at = datetime.utcnow()

    def update(
        self,
        title, date, wind_gust, wind_speed, air_pressure, air_temp,
        **kwargs
    ):
        self.updated_at = datetime.utcnow()
        self.title = title
        self.wind_gust = wind_gust
        self.wind_speed = wind_speed
        self.air_pressure = air_pressure
        self.air_temp = air_temp
        self.sample_date = date

    def __repr__(self):
        return '<Spot {}>'.format(self.title)
