import json
import logging

from flask import Blueprint, jsonify, render_template, request

from app.models import User
from app.schemas import UserSchema
from app import app, db, scraper, recreate_scraper

main = Blueprint('main', __name__)

log = logging.getLogger(__name__)


@main.route('/')
def hello():
    log.info('helo')
    return render_template('hello.html')

@main.route('/reset/')
def reset():
    recreate_scraper()
    return jsonify(True)

@main.route('/login/')
def login():
    creds = json.load(open(app.config['WEBSITE_CREDENTIALS']))
    success = scraper().login(creds['username'], creds['password'])
    return jsonify(success)

@main.route('/spot/')
def spot():
    # TODO test code
    data = scraper().get_spot_data(1786)
    return jsonify(data)
