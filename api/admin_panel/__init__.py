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
from wtforms import Form, BooleanField, StringField, PasswordField, validators

admin_panel = Blueprint('admin_panel', __name__, static_folder='static', template_folder='templates')

REDIS_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
Database = 'LoginPage.db'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for("admin_panel.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@admin_panel.route('/')
@login_required

def index():
    return "Test"

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
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
   
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
class LoginForm(Form):
     username = StringField('Username', [validators.Length(min=4, max=25)])
   
     password = PasswordField('Password', [validators.DataRequired()])

@admin_panel.route('/login', methods=['POST', 'GET'])
def login():
    
    # if request.method == "GET":
    #     return render_template("login.html")
    # else:
    error = None
    form=LoginForm(request.form)
    username = form.username.data
    password = (form.password.data)
    passhash = query_db("select password from login where username = ?", (username,))
    if username is not ""and form.validate():
        if not passhash:
            flash("User does not exist", "danger")
            return render_template("login.html",form=form)
        if sha.verify(password, passhash[0][0]):
            session["username"] = username
            flash("logged in", "danger")
            return redirect(url_for('admin_panel.index'))
        else:
            flash("Incorrect Password", "danger")
            return render_template("login.html",form=form)
    return render_template("login.html",form=form)
@admin_panel.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if query_db("select username from login where username = ?",( form.username.data,)):
        flash("User already taken","danger")
        return render_template("register.html",form=form)
    if request.method == 'POST' and form.validate():
        password = sha.encrypt(form.password.data)
        execute_db("insert into login values(?,?)", (form.username.data,password,))
        flash('Thanks for registering')
        return redirect(url_for('admin_panel.login'))
    return render_template('register.html', form=form)

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

#OLD SIGNUP
# @admin_panel.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == "GET":
#         return render_template("signup.html")
#     else:
#         submission = {"username": request.form["username"], "pass": request.form["password"],
#                       "conf_pass": request.form["conf_pass"]}

#         if submission["pass"] != submission["conf_pass"]:
#             flash("Passwords don't match", "danger")
#             return render_template("signup.html")

#         if query_db("select username from login where username = ?", (submission["username"],)):
#             flash("User already taken", "danger")
#             return render_template("signup.html")
#         if submission["username"]=="":
#             flash("Please enter a valid username")
#             return render_template("signup.html")
#         if submission["pass"]=="":
#             flash("Please enter a valid username")
#             return render_template("signup.html")
#         password = sha.encrypt(submission["pass"])
#         execute_db("insert into login values(?,?)", (submission["username"], password,))
#         flash("User Created", "success")
#         return redirect(url_for("admin_panel.login"))

