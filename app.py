from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = '!secret'

# List all the unique users in the chat
list_chat_users = []

# message data dictionary
message_data = {}


# class to assign a user and the message
class ChatData:
    # constructor
    def __init__(self, name, message_count):
        self.name = name
        self.message_count = message_count


@app.route('/')
def index():
    return render_template('index.html')


# get the custom message event from the client and execute the respective
# function in the server
@socketio.on('my_broadcast_event', namespace='/test')
def broadcast_message(message):
    # check the message payload and if the users is not in list_chat_users
    # then add them to the list
    global list_chat_users
    global message_data

    # get the user from the message from the client
    chat_user = message['data']['user']

    # if the user is not a part of of the list then add him / her to the list
    if chat_user not in list_chat_users:
        list_chat_users.append(chat_user)

        # Instantiate a user and the message count to 1 at the first message
        # from the user
        user = ChatData(chat_user, 1)

        # creating a dictionary in the form of
        # e.g. {'Azeez',1}
        message_data[user.name] = user.message_count
    else:
        # if the user already has sent the message and is in the list chat users
        # update the message count for the user by 1
        # e.g. this would make {'Azeez', 2} on the second message sent by Azeez
        message_data[chat_user] += 1

    emit('my_response', {'data': message['data'], 'd3_data': message_data},
         broadcast=True)


# execute this when the client establishes a connection
@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
