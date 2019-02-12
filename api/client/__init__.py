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
from .requestTypes import RequestTypes
from flask import g
import os
import redis
from worker import celery
import json
import random

client = Blueprint('client', __name__, static_folder='static', template_folder='templates')
REDIS_URL = os.environ.get('REDIS_BROKER_URL', 'redis://localhost:6379/0')


@client.route('/test/')
def test():
    task = celery.send_task('spotify.create_playlist')
    return "Done"

@client.route('/', methods=['GET', 'POST'])
def request_handler():
    if request.method == 'POST':
        if request.is_json:
            req = request.get_json()
            if req['type'] == RequestTypes.add_client:
                new_id = random.getrandbits(128)
                while not valid(new_id):
                    new_id = random.getrandbits(128)
                add_new_id(new_id)
                result = {
                    'status' : 'client created',
                    'id' : new_id
                }
                return json.dumps(result)
            
            if valid(req['id']):
                if req['type'] == RequestTypes.add_vote:
                    pass
        else:
            return 'only json objects accepted'
    else:
        return 'invalid'


def get_redis_db():
    redis_db = getattr(g, '_redis', None)
    if redis_db is None:
        redis_db = g._redis = redis.from_url(REDIS_URL)
    return redis_db

@client.route('/t/')
def tst():
    return 'ass'

@client.route('/test/')
def index():
    value = {
        'a':'A',
        'b':'B'
    }
    redis_set('key',value)
    return str(redis_get('key'))

# FOR REFERENCE
def redis_set(key:str, val):
    value = json.dumps(val)
    get_redis_db().set(key,value)

@client.route('/redis_get/')
def redis_get():
    x = get_redis_db().get('test')
    return x

def valid(id:str):
    id_list = redis_get('id_list')
    if id in id_list:
        return True
    else:
        return False

# requests.post('http://localhost:5000/api/add_message/1234', json={"mytext":"lalala"})
