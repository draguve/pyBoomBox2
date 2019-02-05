from flask import Flask
from flask import url_for
from worker import celery
import celery.states as states

from admin_panel import admin_panel
from client import client

app = Flask(__name__)

app.register_blueprint(admin_panel, url_prefix="/admin")
app.register_blueprint(client, url_prefix="/api")

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
