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

@client.route('/test')
def index():
    return "Test"

# FOR REFERENCE
@client.route('/redis_set/<string:text>')
def redis_set(text):
    get_redis_db().set("test", text)
    return get_redis_db().get('test')

@client.route('/redis_get/')
def redis_get():
    x = get_redis_db().get('test')
    return x

# requests.post('http://localhost:5000/api/add_message/1234', json={"mytext":"lalala"})