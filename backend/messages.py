from database import database
import auth

def get_messages(token, deviceID):
    return database.get_queued_msgs(token, deviceID)

def send_message(token, msg, recipient_name):
    recipientID = database.get_user_by_username(recipient_name)
    print(f"sending to userID: {recipientID}")
    database.add_queued_msg(recipientID, msg)

if __name__ == "__main__":
    print("Testing messages")
    token1, _ = auth.register('user1', 'user1', 'key1_01234567898')
    token2, _ = auth.register('user2', 'user2', 'key2_01234567898')

    print(database.users)

    send_message(token1, "Hi", 'user2')
    print(get_messages(token2, 0))
