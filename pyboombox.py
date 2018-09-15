from flask_script import Manager
from app import create_app
from app.api.spotify import get_token

import os

app = create_app(os.getenv('FLASK_CONFIG') or 'dev')
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