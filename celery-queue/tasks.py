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


@celery.task(name='spotify.current_song')
def create_playlist():
    # TODO: Current actually check the current song
    current_song = spotify.get_track('4HlFJV71xXKIGcU3kRyttv').__dict__
    redis_db.hmset("current_song", current_song)
    return True
