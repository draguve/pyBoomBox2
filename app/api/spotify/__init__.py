from . import internal as spotify
from ... import celery
from ... import cache

#gets the current song from spotify and puts it on the redis server as the key 'current_track'
@celery.task
def update_current_song():
    track = spotify.get_current_track()
    cache.set('current_track',track)

#proxy function for the server init 
def get_token():
    spotify.get_token()
