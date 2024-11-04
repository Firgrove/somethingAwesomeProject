from database import database
import auth

def get_messages(token, deviceID):
    return database.get_queued_msgs(token, deviceID)

def send_message(token, msg, recipient_name, sender):
    i = database.check_token(token)
    if not i:
        raise ValueError("User token not valid")
    
    if database.users[i]["username"] != sender:
        raise ValueError("User token not valid for sender")

    recipientID = database.get_user_by_username(recipient_name)
    print(f"sending to userID: {recipientID}")
    database.add_queued_msg(recipientID, msg, sender)

