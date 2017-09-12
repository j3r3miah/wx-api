import json
import logging

from flask import Blueprint, jsonify, render_template, request

from app.models import Spot
# from app.schemas import UserSchema
from app import app, db

from scraper.service import login as login_task, spot as spot_task

main = Blueprint('main', __name__)

log = logging.getLogger(__name__)


@main.route('/')
def hello():
    log.info('helo')
    return render_template('hello.html')

@main.route('/reset/')
def reset():
    return jsonify(True)

@main.route('/login/')
def login():
    login_task.delay()
    return jsonify(True)

@main.route('/spot/')
def refresh_spot():
    spot_id = 1786
    result = spot_task.delay(spot_id).wait()
    spot = db.session.query(Spot).get(spot_id)
    if spot:
        # TODO SpotSchema
        dump = {k:v for (k,v) in spot.__dict__.items() if k[0] != '_'}
        dump['status'] = result['status']
        return jsonify(dump)
    else:
        return jsonify({'status': result['status']})
