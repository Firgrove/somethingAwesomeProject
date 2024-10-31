from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS

import rsa
import json

from database import database
import auth
import messages

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'hello'

@app.route('/login', methods=['POST'])
def login():
    pass

@app.route('/register', methods=['POST'])
def register():
    pass

@app.route('/logout')
def logout():
    pass

@app.route('/send', methods=['POST'])
def send_msg():
    pass

@app.route('/get_msgs', methods=['GET'])
def get_msgs():
    pass

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), port=6441)