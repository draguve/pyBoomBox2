from worker import celery
import celery.states as states
import os
from admin_panel import admin_panel
from client import client

from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.register_blueprint(admin_panel, url_prefix="/admin")
app.register_blueprint(client, url_prefix="/api")
