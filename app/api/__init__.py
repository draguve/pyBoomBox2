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
from flask import jsonify

import json
import random

from .. import celery
from .. import cache

from . import spotify

api = Blueprint('api', __name__)

@api.route("/celery_test")
def celery_test():
    testing.apply_async(args=["Hello"],countdown=10)
    return 'Testing'

@api.route("/current_track")
def current_track():
    spotify.update_current_song.apply_async(countdown=0)
    track = cache.get('current_track')
    if track==None:
        return jsonify({id:"NotFound"})
    return jsonify(track)

@celery.task
def testing(message):
    print(message)