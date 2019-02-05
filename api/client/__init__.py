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


client = Blueprint('client', __name__, static_folder='static', template_folder='templates')


@client.route('/')
def index():
    return "Test"
