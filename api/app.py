from passlib.hash import sha256_crypt as sha
from worker import celery
import celery.states as states
import sqlite3,os
from admin_panel import admin_panel
from client import client

from flask import Flask, flash, redirect, render_template, request, session, abort , g , url_for , jsonify,send_from_directory

from hashlib import md5
from functools import wraps
from datetime import datetime

import uuid
app = Flask(__name__)

app.register_blueprint(admin_panel, url_prefix="/admin")
app.register_blueprint(client, url_prefix="/api")
Database = 'LoginPage.db'
app.secret_key = os.urandom(12)
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

def query_db(query, args=(), one=False): #used to retrive values from the table
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query , args=()): #executes a sql command like alter table and insert
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query , args)
    conn.commit()
    cur.close()


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        error = None
        username=request.form["username"]
        password=request.form["password"]
        phash = query_db("select password from login where username = ?", (username, ))
        if phash==[]:
            flash("User does not exist","danger")
            return render_template("login.html")

        if sha.verify(password, phash[0][0]):
            flash("User exists")
            session["username"] = username
            flash("logged in","danger")
            return "logged in"
        else:
            flash("Incorrect Password","danger")
            return render_template("login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        submission = {}
        submission["username"] = request.form["username"]
       
        submission["pass"] = request.form["password"]
        submission["conf_pass"] = request.form["conf_pass"]
        

        if submission["pass"]!=submission["conf_pass"]:
            flash("Passwords don't match","danger")
            return render_template("signup.html")

        if query_db("select username from login where username = ?", (submission["username"],))!=[]:
            flash("User already taken","danger")
            return render_template("signup.html")

        password = sha.encrypt(submission["pass"])
        execute_db("insert into login values(?,?)", (submission["username"],password,))
        flash("User Created","success")
        return redirect(url_for("login"))
@app.route('/fuckyou')
def fuck_you():
    return "fuck you"
      

if __name__=='__main__':
    app.run(debug=True)


# let this code stay here for future reference
# @app.route('/add/<int:param1>/<int:param2>')
# def add(param1: int, param2: int) -> str:
#     task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
#     response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
#     return response

# @app.route('/check/<string:task_id>')
# def check_task(task_id: str) -> str:
#     res = celery.AsyncResult(task_id)
#     if res.state == states.PENDING:
#         return res.state
#     else:
#         return str(res.result)
