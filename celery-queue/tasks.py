import os
import spotify
import json
import redis
from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

redis_db = redis.from_url(CELERY_BROKER_URL)
celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='auth.get_url')
def get_url():
    return spotify.get_auth_url()


@celery.task(name='auth.response_url')
def response_url(response):
    return spotify.authenticate_user(response)


@celery.task(name='spotify.create_playlist')
def create_playlist():
    vote_list = []
    # TODO: create the list more smartly
    tracks = spotify.get_playlist_content('spotify', '37i9dQZF1DX6z20IXmBjWI')
    for track in tracks:
        entry = [track, 0]
        vote_list.append(entry)
    redis_db.set('vote_list', json.dumps(vote_list))
    return True
