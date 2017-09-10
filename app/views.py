import json
import logging

from flask import Blueprint, jsonify, render_template, request

from app.models import User
from app.schemas import UserSchema
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
    spot_task.delay(1786)
    return jsonify({})
