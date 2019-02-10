import os
import time
import spotify
from celery import Celery

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='auth.get_url')
def get_url():
    return spotify.get_auth_url()


@celery.task(name='auth.response_url')
def response_url(response):
    return spotify.authenticate_user(response)
