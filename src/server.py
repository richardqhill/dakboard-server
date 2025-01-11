import os

from flask import Flask
from flask_httpauth import HTTPBasicAuth

from huckleberry import get_time_since_last_bottle
from teslamate import get_tesla_stats

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
   os.environ.get('WEB_SERVER_USERNAME'): os.environ.get('WEB_SERVER_PASSWORD')
}
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
def hello_world():
    return "hello world"

@app.route('/bottle', methods=['GET'])
@auth.login_required
def bottle():
    return get_time_since_last_bottle()

@app.route('/tesla', methods=['GET'])
@auth.login_required
def tesla():
    return get_tesla_stats()

if __name__ == '__main__':
    app.run(port=8000)