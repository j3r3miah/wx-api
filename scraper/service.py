import os
import json
import atexit
import logging

from celery import Celery

from scraper.scraper import Scraper

# logging.basicConfig(
#     level=logging.INFO,
#     datefmt='%Y-%m-%d %H:%M:%S',
#     format='%(asctime)s - [%(levelname)s] %(message)s'
# )

log = logging.getLogger(__name__)

# db = SQLAlchemy(app)

_scraper = None

app = Celery(
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

@app.task
def reset():
    _scraper_destroy()
    _scraper_init()

@app.task
def login():
    reset()
    creds = json.load(open(os.environ['WEBSITE_CREDENTIALS']))
    success = _scraper.login(creds['username'], creds['password'])
    return success

@app.task
def spot(spot_id):
    data = _scraper.get_spot_data(spot_id)
    return data
