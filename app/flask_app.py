import os
import enum
import datetime as dt

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_at = db.Column(db.DateTime())

    def __init__(self, name):
        self.name = name
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<User id {}>'.format(self.id)


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    created_at = fields.DateTime()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/<name>')
def hello_name(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return _mkstr(name)


@app.route('/users/')
def users():
    all_users = db.session.query(User).all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@app.route('/users/<id>')
def user_detail(id):
    user = db.session.query(User).get(id)
    return jsonify(user_schema.dump(user).data)


# prove we are running python 3
def _mkstr(name: str) -> str:
    return 'Hello {}'.format(name)
