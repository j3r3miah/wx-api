import os
import enum

from flask import render_template
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/<name>')
def hello_name(name):
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return mkstr(name)


# prove we are running python 3
def mkstr(name: str) -> str:
    return 'Hello {}'.format(name)
