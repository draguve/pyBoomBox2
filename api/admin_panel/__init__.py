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
from flask import g

from functools import wraps
from passlib.hash import sha256_crypt as sha
import sqlite3
import redis
import os

from worker import celery
import celery.states as states

admin_panel = Blueprint('admin_panel', __name__, static_folder='static', template_folder='templates')

REDIS_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
Database = 'LoginPage.db'


@admin_panel.route('/')
def index():
    return "Test"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(Database)
    return db


def query_db(query, args=(), one=False):  # used to retrive values from the table
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=()):  # executes a sql command like alter table and insert
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()


def get_redis_db():
    redis_db = getattr(g, '_redis', None)
    if redis_db is None:
        redis_db = g._redis = redis.from_url(REDIS_URL)
    return redis_db


@admin_panel.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        error = None
        username = request.form["username"]
        password = request.form["password"]
        passhash = query_db("select password from login where username = ?", (username,))
        if not passhash:
            flash("User does not exist", "danger")
            return render_template("login.html")

        if sha.verify(password, passhash[0][0]):
            flash("User exists")
            session["username"] = username
            flash("logged in", "danger")
            return "logged in"
        else:
            flash("Incorrect Password", "danger")
            return render_template("login.html")


@admin_panel.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        submission = {"username": request.form["username"], "pass": request.form["password"],
                      "conf_pass": request.form["conf_pass"]}

        if submission["pass"] != submission["conf_pass"]:
            flash("Passwords don't match", "danger")
            return render_template("signup.html")

        if query_db("select username from login where username = ?", (submission["username"],)):
            flash("User already taken", "danger")
            return render_template("signup.html")

        password = sha.encrypt(submission["pass"])
        execute_db("insert into login values(?,?)", (submission["username"], password,))
        flash("User Created", "success")
        return redirect(url_for("admin_panel.login"))


@admin_panel.route('/get_url')
def get_url():
    task = celery.send_task('auth.get_url')
    response = f"<a href='{url_for('admin_panel.check_task', task_id=task.id, external=True)}'>" \
        f"check status of {task.id} </a>"
    return response


@admin_panel.route('/auth_url', methods=['POST', 'GET'])
def auth_url():
    if request.method == 'POST':
        url = request.form['response']
        task = celery.send_task('auth.response_url', args=[url, ], kwargs={})
        response = f"<a href='{url_for('admin_panel.check_task', task_id=task.id, external=True)}'>" \
            f"check status of {task.id} </a>"
        return response
    else:
        return render_template('auth_url_form.j2')


@admin_panel.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)

# FOR REFERENCE
# @admin_panel.route('/redis_set/<string:text>')
# def redis_set(text):
#     get_redis_db().set("test", text)
#     return 'set'
#
#
# @admin_panel.route('/redis_get')
# def redis_get():
#     x = get_redis_db().get('test')
#     return x
