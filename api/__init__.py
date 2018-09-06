
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

import spotipy
import spotipy.util as util

api = Blueprint('api', __name__)

username = 'username'
client_id='clientid'
client_secret='clientsecret'
redirect_uri='redirecturl'


def get_token():
    scope = 'playlist-modify-private'
    token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    return token

@api.route("/get_token/")
def token():
    return get_token()

