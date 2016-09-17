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


# class to assign a user and the message
class ChatData:
    # constructor
    def __init__(self, name, message_count):
        self.name = name
        self.message_count = message_count


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('my_broadcast_event', namespace='/test')
def broadcast_message(message):
    # check the message payload and if the users is not in list_chat_users
    # then add them to the list
    global list_chat_users
    global message_data
    global msg_data_list

    # get the user from the message from the client
    chat_user = message['data']['user']

    # if the user is not a part of of the list then add him / her to the list
    if chat_user not in list_chat_users:
        list_chat_users.append(chat_user)

        # Instantiate a user and the message count to 1 at the first message
        # from the user
        user = ChatData(chat_user, 1)

        # creating a dictionary in the form of
        # e.g. {'user':{'name':'Azeez', 'msg_count':1}}

        message_data['user']['name'] = user.name
        message_data['user']['msg_count'] = user.message_count

        # add it to the msg_data_list
        msg_data_list.append(message_data)
        # convert the list to json format
        json.dumps(msg_data_list)
        # reset the nested dictionary
        message_data = {'user': {}}
        print msg_data_list

    else:
        # if the user already has sent the message and is in the list chat users
        # update the message count for the user by 1
        # iterate thru the list of dictionaries
        for dict_items in msg_data_list:
            # iterate thru the dictionary
            for key, value in dict_items['user'].iteritems():
                # increment the msg count by 1 for the user who sends a message
                if dict_items['user']['name'] == chat_user:
                    dict_items['user']['msg_count'] += 1
                    print json.dumps(msg_data_list)
                # if the msg count is incremented by 1, break the loop
                # as we don't have to loop thru the rest of the dictionary
                break

    # send the chat message back to the client and send the chat metrics data
    emit('my_response', {'data': message['data'], 'd3_data':
        msg_data_list},
         broadcast=True)


# execute this when the client establishes a connection
@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
