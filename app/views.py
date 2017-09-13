import json
import logging

from flask import Blueprint, jsonify, render_template, request

from app.models import Spot
# from app.schemas import UserSchema
from app import app, db

from scraper.service import touch_spot as touch_spot_task

main = Blueprint('main', __name__)

log = logging.getLogger(__name__)


@main.route('/')
def hello():
    log.info('helo')
    return render_template('hello.html')

@main.route('/spot/')
def get_spot():
    spot_id = 1786
    touch_spot_task.delay(spot_id)
    spot = db.session.query(Spot).get(spot_id)
    if spot:
        # TODO SpotSchema
        dump = {k:v for (k,v) in spot.__dict__.items() if k[0] != '_'}
        dump['status'] = 'whatever'
        return jsonify(dump)
    else:
        return jsonify({'status': 'ask_again_later'})
