import app.api.spotify as spotify
from ... import celery

#gets the current song from spotify and puts it on the redis server as the key 'current_track'
@celery.task
def get_current_song():
    track = spotify.get_current_track()
