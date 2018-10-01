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

import json
import random

from .. import celery

api = Blueprint('api', __name__)

@api.route("/celery_test")
def celery_test():
    testing.apply_async(args=["Hello"],countdown=10)
    return 'Testing'

@celery.task
def testing(message):
    print(message)

