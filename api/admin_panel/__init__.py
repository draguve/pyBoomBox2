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


admin_panel = Blueprint('admin_panel', __name__, static_folder='static', template_folder='templates')

@admin_panel.route('/')
def index():
    return "Test"