from database import database

import random
import string
import hashlib

letters = string.ascii_letters
TOKEN_LEN = 128

'''
Takes username and password to log in. If the device has already been used, takes deviceID
Otherwise takes a pub_key and adds the device to the list of user's devices
Returns the deviceID so if this is the first time this device has logged in, it can store its own ID
'''
def login(username, password, deviceID, pub_key):
    password = password.encode('utf-8')
    password = hashlib.sha256(password)

    uID = database.check_login(username, password)
    if not uID:
        raise ValueError("Username or password are not valid")

    # Generate token
    token = ''.join(random.choice(letters) for i in range(TOKEN_LEN))
    # Verify we haven't accidentally created a duplicate token. If we have regenerate it
    while database.check_token(token):
        token = ''.join(random.choice(letters) for i in range(TOKEN_LEN))

    # If we're registering a new device
    if deviceID == None:
        deviceID = database.add_device(uID, token, pub_key)
    else:
        database.add_token(uID, token, deviceID)

    return token, deviceID


def register(username, password, pub_key):
    password = password.encode('utf-8')
    password = hashlib.sha256(password)

    if database.get_user_by_username(username):
        raise ValueError("Username already in use")
    
    uID = database.register(username, password, pub_key)

    # Generate token
    token = ''.join(random.choice(letters) for i in range(TOKEN_LEN))
    # Verify we haven't accidentally created a duplicate token. If we have regenerate it
    while database.check_token(token):
        token = ''.join(random.choice(letters) for i in range(TOKEN_LEN))

    database.add_token(uID, token, 0)

    return token, 0
    

def logout(token):
    database.logout(token)


if __name__ == "__main__":
    print("Testing auth.py")
    register("test", "test", "key")
    print(f'User database: {database.users}')