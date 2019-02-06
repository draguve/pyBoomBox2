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

from worker import celery
import celery.states as states

admin_panel = Blueprint('admin_panel', __name__, static_folder='static', template_folder='templates')


@admin_panel.route('/')
def index():
    return "Test"


@admin_panel.route('/get_url')
def get_url():
    task = celery.send_task('auth.get_url')
    response = f"<a href='{url_for('admin_panel.check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response


@admin_panel.route('/auth_url', methods=['POST', 'GET'])
def auth_url():
    if request.method == 'POST':
        url = request.form['response']
        task = celery.send_task('auth.response_url', args=[url, ], kwargs={})
        response = f"<a href='{url_for('admin_panel.check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
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

