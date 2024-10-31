import random

'''
Users are dicts in the form:
{
    "uID": Int,
    "username": Str
    "pass": Str,            # Hash of user's password
    "devices": [{
                    "deviceID": Int
                    "token": Str,           # Token for the session. Can be none if user is not logged in
                    "pub_key": Str,
                    "queued_messages"
                }]
}
'''

users = []

'''
Helper functions
'''
def get_user_by_id(id):
    for user in users:
        if user["uID"] == id:
            return user
    
    return None

def get_user_by_username(name):
    for user in users:
        if user["username"] == name:
            return user
    
    return None

'''
Backend interface functions
'''

def register(name, hashed_pass, pub_key):
    if get_user_by_username(name):
        raise ValueError("Username already in use")
    
    uID = random.randint(0, 10000000)
    while get_user_by_id(uID):
        random.randint(0, 10000000)

    user_dict ={
        "uID": uID,
        "username": name,
        "pass": hashed_pass,
        "devices": [{
                "deviceID": 0,
                "token": None,
                "pub_key": pub_key,
                "queued_messages": []
            }]
    }

    users.append(user_dict)

def add_token(uID, token, device):
    pass

def add_device(uID, pub_key):
    pass

# Check to see if a token is valid and if it is return the user id
def check_oken(token):
    pass


def get_queued_msgs(uID, deviceID):
    pass

# Adds message to the queue for each device
def add_queued_msg(uID, msg):
    pass