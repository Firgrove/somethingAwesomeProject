import random
import bcrypt
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP

from base64 import b64decode,b64encode

'''
Users are dicts in the form:
{
    "uID": Int,
    "username": Str
    "pass": Str,            # Hash of user's password
    "devices": [{
                    "token": Str,           # Token for the session. Can be none if user is not logged in
                    "pub_key": Str,
                    "queued_messages"
                }]
}
'''

print("---------- Starting Database ----------")

users = [{
    "uID": 0,
    "username": "admin",
    "pass": "admin",
    "devices": [{
        "token": "token",
        "pub_key": "test_key",
        "queued_messages": []
    }]
}]

MAX_USERS = 10000000

'''
Helper functions

Returns tuple of user's index in database and user dict
'''
def get_user_by_id(uID):
    return next((index for (index, user) in enumerate(users) if user["uID"] == uID), None)

'''
Same as above but by username
'''
def get_user_by_username(name):
    return next((user["uID"] for (index, user) in enumerate(users) if user["username"] == name), None)

def encrypt(msg, externKey):
    msg = str.encode(msg)
    public_key = RSA.importKey(externKey)
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted = encryptor.encrypt(msg)
    return encrypted

'''
Backend interface functions
'''

def register(name, hashed_pass, pub_key):
    if get_user_by_username(name):
        raise ValueError("Username already in use")
    
    uID = random.randint(0, MAX_USERS)
    while get_user_by_id(uID):
        random.randint(0, MAX_USERS)

    user_dict ={
        "uID": uID,
        "username": name,
        "pass": hashed_pass,
        "devices": [{
                "token": None,
                "pub_key": pub_key,
                "queued_messages": []
            }]
    }

    users.append(user_dict)

    return uID

def check_login(username, password):
    for i, user in enumerate(users):
        print(user["username"])
        if user["username"] == username:
            print(user)
            print(bcrypt.checkpw(password, user["pass"]))
            return user["uID"]
    
    return None

def add_token(uID, token, deviceID):
    i = get_user_by_id(uID)
    if i == None:
        raise ValueError("User ID or Device ID not valid")
    
    if deviceID >= len(users[i]["devices"]):
        raise ValueError("User ID or Device ID not valid")
    
    # If user is logged in with another session, invalidates that session
    users[i]["devices"][deviceID]["token"] = token


def add_device(uID, token, pub_key):
    i = get_user_by_id(uID)
    if i == None:
        raise ValueError("User does not exist")
    
    users[i]["devices"].append({
        "token": token,
        "pub_key": pub_key,
        "queued_messages": []
    })

    return len(users[i]["devices"])-1

# Check to see if a token is valid and if it is return the user id
def check_token(token):
    for i, user in enumerate(users):
        for device in user["devices"]:
            if device["token"] == token:
                return i

    return None

def logout(token):
    i = check_token(token)
    if i == None:
        return
    
    for j in range(len(users[i]["devices"])):
        if users[i]["devices"][j]["token"] == token:
            users[i]["devices"][j]["token"] = None
            break

def get_queued_msgs(token, deviceID):
    i = check_token(token)
    if i == None:
        raise ValueError("Invalid Token")
    
    msgs = users[i]["devices"][deviceID]["queued_messages"]
    users[i]["devices"][deviceID]["queued_messages"] = []
    return msgs


# Adds message to the queue for each device
def add_queued_msg(uID, msg, sender):
    i = get_user_by_id(uID)
    if i == None:
        raise ValueError("uID does not exist")
    
    for j, device in enumerate(users[i]["devices"]):
        key = device["pub_key"]
        encrypted_msg = encrypt(msg, key)

        msg_dict = {
            "encrypted_msg": encrypted_msg,
            "sender": sender
        }

        users[i]["devices"][j]["queued_messages"].append(encrypted_msg)

if __name__ == "__main__":
    print("testing")
    print(get_user_by_id(0))
    print(users)

    new_key = RSA.generate(2048)
    print(new_key)
    
    public_key = new_key.publickey().exportKey("DER")
    print(encrypt('hi', public_key))

    # add_queued_msg(0, public_key)