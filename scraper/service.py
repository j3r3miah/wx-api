import os
import json
import atexit
import logging
from datetime import timedelta

from celery import Celery
from celery.task import periodic_task

from flask_sqlalchemy import SQLAlchemy

from scraper.scraper import Scraper

from app import db
from app.models import Spot

log = logging.getLogger(__name__)

worker = Celery(
    __name__,
    backend='rpc://',
    broker='amqp://guest:guest@amqp:5672//'
)

_scraper = None

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

@worker.task
def login():
    _scraper_destroy()
    _scraper_init()
    creds = json.load(open(os.environ['WEBSITE_CREDENTIALS']))
    success = _scraper.login(creds['username'], creds['password'])
    return success

def ensure_login():
    global _scraper
    if not _scraper:
        login()

@worker.task
def touch_spot(spot_id):
    spot = db.session.query(Spot).get(spot_id)
    if spot:
        spot.touch()
    else:
        spot = Spot()
        spot.id = spot_id
        db.session.add(spot)
    db.session.commit()

@worker.task
def refresh_spot(spot_id):
    _refresh_spot(db.session.query(Spot).get(spot_id))

# @worker.task
@periodic_task(run_every=timedelta(seconds=30))
def auto_refresh_loop():
    log.info('[autorefresh] Scanning for spots to refresh')
    for spot in db.session.query(Spot).all():
        if spot.should_refresh() and spot.needs_refresh():
            log.info('[autorefresh] Refreshing spot: %s' % spot.id)
            _refresh_spot(spot)

def _refresh_spot(spot):
    ensure_login()
    data = _scraper.get_spot_data(spot.id)
    spot.update(**data)
    db.session.commit()
    return data
