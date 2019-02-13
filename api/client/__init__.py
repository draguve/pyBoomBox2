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
REDIS_URL = os.environ.get('REDIS_BROKER_URL', 'redis://192.168.137.54:7777/0')

# def test():
#     task = celery.send_task('tasks.add')
#     response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
#     return True

def add_new_id():
    new_id = random.getrandbits(128)
    while valid(new_id):
        new_id = random.getrandbits(128)
    id_list = redis_get('id_list')
    id_list.update(new_id)
    redis_set('id_list',id_list)
    return new_id

# TODO: test when redis server available
def add_vote(song:str):
    song_list = redis_get('song_list')
    if song in song_list:
        song_list['song'] += 1
        return json.dumps({'status' : 'vote added'})
    else:
        return json.dumps({'status' : 'song not up for voting'})


@client.route('/', methods=['GET', 'POST'])
def request_handler():
    if request.method == 'POST':
        if request.is_json:
            req = request.get_json()
            if req['type'] == RequestTypes.add_client.value: # vulnerable to DOS
                new_id = add_new_id()
                result = {
                    'status' : 'client created',
                    'id' : new_id
                }
                return json.dumps(result)
            elif valid(req['id']):
                if req['type'] == RequestTypes.add_vote.value:
                    return add_vote(req['song'])
        else:
            return 'only json objects accepted'
    else:
        return 'invalid'

def get_redis_db():
    redis_db = getattr(g, '_redis', None)
    if redis_db is None:
        redis_db = g._redis = redis.from_url(REDIS_URL)
    return redis_db

def redis_set(key:str, val):
    value = json.dumps(val)
    get_redis_db().set(key,value)

def redis_get(key:str):
    value = get_redis_db().get(key)
    return json.loads(value)

def valid(id:str):
    id_list = redis_get('id_list')
    if id in id_list:
        return True
    else:
        return False

# requests.post('http://localhost:5000/api/', json={"type":1})