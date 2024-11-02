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
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    deviceID = request.get_json().get('deviceID')
    pub_key = request.get_json().get('pub_key')

    token, deviceID = auth.login(username, password, deviceID, pub_key)

    return jsonify({
        "token": token,
        "deviceID": deviceID
    })

@app.route('/register', methods=['POST'])
def register():
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    pub_key = request.get_json().get('pub_key')

    token, deviceID = auth.register(username, password, pub_key)

    return jsonify({
        "token": token,
        "deviceID": deviceID
    })

@app.route('/logout')
def logout():
    token = request.get_json().get('token')

    auth.login(token)

@app.route('/send', methods=['POST'])
def send_msg():
    pass

@app.route('/get_msgs', methods=['GET'])
def get_msgs():
    pass

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), port=6441)