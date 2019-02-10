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
from .requestTypes import RequestTypes

client = Blueprint('client', __name__, static_folder='static', template_folder='templates')

@client.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            if request.get_json()['type'] == RequestTypes.addVote:
                pass
        else:
            return request.form['firstname'] + " is a bitch"
    else:
        return """
        <form action="/api"  method="post">
            First name:<br>
            <input type="text" name="firstname" value=""><br>
            Last name:<br>
            <input type="text" name="lastname" value=""><br><br>
            <input type="submit" value="Submit">
        </form> 
        """


# requests.post('http://localhost:5000/api/add_message/1234', json={"mytext":"lalala"})