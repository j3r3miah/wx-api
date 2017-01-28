import os

from flask import Flask

from .database import configure_db
from .views import main as main_blueprint


def uwsgi_main():
    app = create_app()
    configure_db(app)
    return app


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(main_blueprint)
    return app
