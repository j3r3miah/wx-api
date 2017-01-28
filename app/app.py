import os

from flask import Flask, jsonify, render_template

from database import init_db
from models import User
from schemas import UserSchema


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app.config['SQLALCHEMY_DATABASE_URI'])

# init_db() defines db_session, so import it now
from database import db_session


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/<name>')
def hello_name(name):
    user = User(name=name)
    db_session.add(user)
    db_session.commit()
    return user_detail(user.id)


@app.route('/users/')
def users():
    all_users = db_session.query(User).all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


@app.route('/users/<id>')
def user_detail(id):
    user = db_session.query(User).get(id)
    return jsonify(user_schema.dump(user).data)
