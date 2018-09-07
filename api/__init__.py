
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
from spotipy.oauth2 import SpotifyClientCredentials

import json
import random

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

def get_random_playlists(limit=1,offset=-1):
    if(offset==-1):
        offset = random.randint(0,1500)
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists = sp.user_playlists('spotify',limit=limit,offset=offset)
    return playlists

@api.route("/get_random_playlist")
def get_random_playlist():
    return json.dumps(get_random_playlists(limit=5))