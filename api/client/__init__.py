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
REDIS_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')


@client.route('/test/')
def test():
    task = celery.send_task('spotify.create_playlist')
    return "Done"


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
