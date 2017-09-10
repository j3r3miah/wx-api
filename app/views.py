import json
import logging

from flask import Blueprint, jsonify, render_template, request

from app.models import User
from app.schemas import UserSchema
from app import app, db

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
    return jsonify(True)

@main.route('/spot/')
def spot():
    return jsonify({})
