from flask import Flask
from flask_script import Manager

from webui import webui
from api import api

app = Flask(__name__)
app.register_blueprint(webui)
app.register_blueprint(api, url_prefix="/api")
manager = Manager(app=app)

@app.after_request
def headers(response):
    response.headers["Server"] = "pyBoomBox"
    return response

if __name__ == "__main__":
    manager.run()