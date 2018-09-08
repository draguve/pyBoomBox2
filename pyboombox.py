from flask import Flask
from flask_script import Manager

from webui import webui
from api import api
from api.spotify import get_token

from config import config

#importing api and webui
app = Flask(__name__)
app.config.from_object(config['dev'])
app.register_blueprint(webui)
app.register_blueprint(api, url_prefix="/api")
manager = Manager(app=app)

@app.after_request
def headers(response):
    response.headers["Server"] = "pyBoomBox"
    return response

@manager.command
def inittoken():
    thing = get_token()
    
if __name__ == "__main__":
    manager.run()