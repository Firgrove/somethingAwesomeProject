from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS

import rsa
import json

from database import database
import auth
import messages

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request_func(response):
  response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
  return response

@app.route('/')
def hello():
    return 'hello'

@app.route('/login', methods=['POST'])
def login():
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    deviceID = request.get_json().get('deviceID')
    pub_key = request.get_json().get('pub_key')

    print(database.users)

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
    token = request.get_json().get('token')
    msg = request.get_json().get('msg')
    sender = request.get_json().get('sender')
    recipient_name = request.get_json().get('recipient')
    messages.send_message(token, msg, recipient_name, sender)

@app.route('/get_msgs', methods=['GET'])
def get_msgs():
    token = request.get_json().get('token')
    device = request.get_json().get('deviceID')

    return jsonify({
        "messages": get_msgs(token, device)
    })

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), port=6441)