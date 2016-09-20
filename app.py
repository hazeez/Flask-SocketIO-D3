from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = '!secret'

# List all the unique users in the chat
list_chat_users = []

# message data dictionary
message_data = {'user': {}}

# message user list
# empty list to store all the chat metrics
msg_data_list = []

# set the color for each user - for d3 to fill a circle for a user
colors = ["blue", "pink", "red", "orange", "green"]

# set the user count to 0
user_count = 0

# set the total message count to 0
total_messages = 0


# class to assign a user and the message
class ChatData:
    # constructor
    def __init__(self, number, name, message_count, user_color):
        self.number = number
        self.name = name
        self.message_count = message_count
        self.color = user_color


@app.route('/')
def index():
    return render_template('index.html')


# execute this when the client establishes a connection
@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected'})


@socketio.on('my_broadcast_event', namespace='/test')
def broadcast_message(message):
    # check the message payload and if the users is not in list_chat_users
    # then add them to the list
    global list_chat_users
    global message_data
    global msg_data_list
    global user_count
    global total_messages

    # get the user from the message from the client
    chat_user = message['data']['user']

    # if the user is not a part of of the list then add him / her to the list
    if chat_user not in list_chat_users:
        # increment the user by 1
        user_count += 1
        total_messages += 1

        # add them to the user list
        list_chat_users.append(chat_user)

        # Instantiate a user and the message count to 1 at the first message
        # from the user
        user = ChatData(user_count, chat_user, 1, colors[user_count - 1])

        # creating a dictionary in the form of
        # e.g. {'user':{'num':1, 'name':'Azeez', 'msg_count':1, "color":blue}}

        message_data['user']['num'] = user.number
        message_data['user']['name'] = user.name
        message_data['user']['msg_count'] = user.message_count
        message_data['user']['color'] = user.color

        # add it to the msg_data_list
        msg_data_list.append(message_data)
        # reset the nested dictionary
        message_data = {'user': {}}
        print msg_data_list

    else:
        # if the user already has sent the message and is in the list chat users
        # increment the total messages by 1
        total_messages += 1
        # update the message count for the user by 1
        # iterate thru the list of dictionaries
        for dict_items in msg_data_list:
            # iterate thru the dictionary
            for key, value in dict_items['user'].iteritems():
                # increment the msg count by 1 for the user who sends a message
                if dict_items['user']['name'] == chat_user:
                    dict_items['user']['msg_count'] += 1
                    print msg_data_list
                # if the msg count is incremented by 1, break the loop
                # as we don't have to loop thru the rest of the dictionary
                break

    # send the chat message back to the client and send the chat metrics data
    emit('my_response', {'data': message['data'], 'd3_data': msg_data_list,
                         'total_messages': total_messages}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
