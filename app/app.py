import os

from flask import Flask

from database import configure_db
from views import create_views


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    configure_db(app)
    create_views(app)

    return app
