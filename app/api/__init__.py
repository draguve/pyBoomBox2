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

import json
import random

import app.api.spotify
from .. import celery

api = Blueprint('api', __name__)

username = 'username'
client_id='clientid'
client_secret='clientsecret'
redirect_uri='redirecturl'

@api.route("/get_token/")
def token():
    return spotify.get_token()

@api.route("/get_random_playlist")
def get_random_playlist():
    return json.dumps(spotify.get_random_playlists(limit=5))

@api.route("/celery_test")
def celery_test():
    send_async_email.apply_async(args=[msg], countdown=60)
    testing.apply_async(args=["Hello"],countdown=10)
    return 'Testing'

@celery.task
def testing(message):
    print(message)

