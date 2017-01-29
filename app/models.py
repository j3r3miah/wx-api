import datetime as dt
from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    created_at = Column(DateTime)

    def __init__(self, name):
        self.name = name
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<User {}>'.format(self.name)
