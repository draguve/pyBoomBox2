import random
import string

class Config:
    SECRET_KEY = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(60))
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}