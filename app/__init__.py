import os
import json
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - [%(levelname)s] %(message)s'
)

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def create_app():
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
