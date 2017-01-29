from flask import Blueprint, jsonify, render_template, g

from .models import User
from .schemas import UserSchema
from . import db


main = Blueprint('main', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@main.route('/')
def hello():
    return render_template('hello.html')


@main.route('/<name>')
def hello_name(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return user_detail(user.id)


@main.route('/users/')
def users():
    all_users = db.session.query(User).all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@main.route('/users/<id>')
def user_detail(id):
    user = db.session.query(User).get(id)
    return jsonify(user_schema.dump(user).data)
