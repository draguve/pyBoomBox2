from flask import Flask
from flask import url_for
from worker import celery
from worker import cache
import celery.states as states

from admin_panel import admin_panel
from client import client

app = Flask(__name__)
cache.init_app(app)

app.register_blueprint(admin_panel, url_prefix="/admin")
app.register_blueprint(client, url_prefix="/api")
