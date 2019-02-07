from flask import Blueprint
from flask import abort
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
from flask import send_from_directory
from flask import current_app

import os
import redis

client = Blueprint('client', __name__, static_folder='static', template_folder='templates')
REDIS_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')


def get_redis_db():
    redis_db = getattr(g, '_redis', None)
    if redis_db is None:
        redis_db = g._redis = redis.from_url(REDIS_URL)
    return redis_db


@client.route('/')
def index():
    return "Test"

# FOR REFERENCE
# @admin_panel.route('/redis_set/<string:text>')
# def redis_set(text):
#     get_redis_db().set("test", text)
#     return 'set'
#
#
# @admin_panel.route('/redis_get')
# def redis_get():
#     x = get_redis_db().get('test')
#     return x
