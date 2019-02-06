import os
from celery import Celery
from flask_caching import Cache

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# TODO: Please Fix hardcoded redis host link               | this
cache_config = {'CACHE_TYPE': 'redis','CACHE_REDIS_HOST': 'redis'}
cache = Cache(config=cache_config)
