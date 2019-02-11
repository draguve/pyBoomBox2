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

client = Blueprint('client', __name__, static_folder='static', template_folder='templates')
REDIS_URL = os.environ.get('REDIS_BROKER_URL', 'redis://localhost:6379/0')
def test():
    task = celery.send_task('tasks.add')
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return True
@client.route('/', methods=['GET', 'POST'])
def request_handler():
    if request.method == 'POST':
        if request.is_json:
            req = request.get_json()
            if is_valid(req['id']):
                if req['type'] == RequestTypes.addVote:
                    pass
        else:
            return request.form['firstname'] + " is a bitch"
    else:
        return 'invalid'
        # """
        # <form action="/api"  method="post">
        #     First name:<br>
        #     <input type="text" name="firstname" value=""><br>
        #     Last name:<br>
        #     <input type="text" name="lastname" value=""><br><br>
        #     <input type="submit" value="Submit">
        # </form>
        # """

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
    print(redis_get('key'))

# FOR REFERENCE
def redis_set(key:str, val):
    value = json.dumps(val)
    get_redis_db().set(key,value)

def redis_get(key:str):
    value = get_redis_db().get(key)
    return json.loads(value)

def is_valid(id:str):
    id_list = redis_get('id_list')

# requests.post('http://localhost:5000/api/add_message/1234', json={"mytext":"lalala"})