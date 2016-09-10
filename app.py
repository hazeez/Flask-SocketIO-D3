from flask import Flask, render_template
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = '!secret'


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('my_broadcast_event', namespace='/test')
def broadcast_message(message):
    emit('my_response', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected'})


if __name__ == '__main__':
    socketio.run(app)
