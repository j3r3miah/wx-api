import os
import json
import atexit
import logging
import datetime as dt

from celery import Celery
from flask_sqlalchemy import SQLAlchemy

from scraper.scraper import Scraper

from app import db
from app.models import Spot

log = logging.getLogger(__name__)

_scraper = None

worker = Celery(
    __name__,
    backend='rpc://',
    broker='amqp://guest:guest@amqp:5672//'
)

def _scraper_init():
    global _scraper
    if not _scraper:
        log.info('creating scraper')
        _scraper = Scraper(
            os.environ['CHROME_DRIVER_PATH'],
            os.environ['SCRAPER_DATA_DIR'],
            json.load(open(os.environ['WEBSITE_URLS']))
        )

def _scraper_destroy():
    global _scraper
    if _scraper:
        log.info('destroying scraper')
        _scraper.shutdown()
        _scraper = None

# atexit.register(_scraper_quit)

@worker.task
def reset():
    _scraper_destroy()
    _scraper_init()

@worker.task
def login():
    reset()
    creds = json.load(open(os.environ['WEBSITE_CREDENTIALS']))
    success = _scraper.login(creds['username'], creds['password'])
    return success

_last_update = {}

@worker.task
def spot(spot_id):
    last_update = _last_update.get(spot_id)
    if (
        last_update and
        last_update + dt.timedelta(minutes=1) > dt.datetime.utcnow()
    ):
        _last_update[spot_id] = dt.datetime.utcnow()
        print('queuing a refresh')
        refresh_spot.delay(spot_id)
        return {'status': 'refreshing'}

    # return status (first_load, refreshing, up_to_date, etc)
    print('spot is already up to date')
    return {'status': 'up_to_date'}

@worker.task
def refresh_spot(spot_id):
    data = _scraper.get_spot_data(spot_id)
    spot = db.session.query(Spot).get(spot_id)
    if not spot:
        spot = Spot()
        spot.id = spot_id
        db.session.add(spot)
    spot.update(**data)
    print(spot)
    print(spot.__dict__)
    db.session.commit()
    print(db.session.query(Spot).all())
    return data
