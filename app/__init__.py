import os
import json
import atexit
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.scraper import Scraper

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

_scraper = None

def _scraper_quit():
    if _scraper:
        log.info('destroying scraper')
        _scraper.shutdown()

atexit.register(_scraper_quit)


def create_app():
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

def scraper():
   return _scraper

def recreate_scraper():
    global _scraper
    _scraper_quit()
    log.info('creating scraper')
    _scraper = Scraper(
        app.config['CHROME_DRIVER_PATH'],
        app.config['SCRAPER_DATA_DIR'],
        json.load(open(app.config['WEBSITE_URLS']))
    )

recreate_scraper()
