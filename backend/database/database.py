import random

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
        "token": "token"
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
    i = next((index for (index, user) in enumerate(users) if user["username"] == name), None)

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
        if user["username"] == username and user["password"] == password:
            return user["uID"]
    
    return None

def add_token(uID, token, deviceID):
    i = get_user_by_id(uID)
    if not i:
        raise ValueError("User ID or Device ID not valid")
    
    if deviceID >= len(users[i]["devices"]):
        raise ValueError("User ID or Device ID not valid")
    
    # If user is logged in with another session, invalidates that session
    users[i]["devices"][deviceID]["token"] = token


def add_device(uID, token, pub_key):
    i = get_user_by_id(uID)
    if not i:
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
    if not i:
        return
    
    for j in range(len(users[i]["device"])):
        if users[i]["device"][j]["token"] == token:
            users[i]["device"][j]["token"] = None
            break

def get_queued_msgs(token, deviceID):
    i = check_token(token)
    if not i:
        raise ValueError("Invalid Token")
    
    return users[i]["devices"][deviceID]["queued_messages"]


# Adds message to the queue for each device
def add_queued_msg(uID, msg):
    i = get_user_by_id(uID)
    if not i:
        raise ValueError("uID does not exist")
    
    for j in range(users[i]["devices"]):
        #TODO: Compute hash of message with each devices private key before adding it to the queue
        users[i]["devices"][j]["queued_messages"].append(msg)

if __name__ == "__main__":
    print("testing")
    print(get_user_by_id(0))