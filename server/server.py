import logging
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from twitch_chat_irc import twitch_chat_irc

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*", namespace="/twitch")
socketio.init_app(app, cors_allowed_origins="*")  # Bind SocketIO with Flask app

LOG = logging.getLogger(__name__)

CORS(app)

chat_messages = []

def twitch_message_received(msg):
    logging.debug(msg)
    logging.debug(msg["color"])
    logging.debug(msg["display-name"])
    logging.debug(msg["message"])

    if msg["color"] != "":
        color = tuple(int(msg["color"].lstrip("#")[i: i + 2], 16) for i in (0, 2, 4))
    else:
        color = (218, 165, 32)
    logging.debug(color)

    to_send = {
        "content": msg["message"],
        "displayName": msg["display-name"],
        "roles": [{
            "colorR": color[0],
            "colorG": color[1],
            "colorB": color[2],
            "icon": None,
            "id": 1,
            "name": "Twitch Chatter",
        }],
        "stickers": [],
        "emojis": [],
        "mentions": [],
        "author_id": msg["user-id"],
        "platform": "twitch",
    }
    # print content and author
    print(to_send["displayName"], to_send["content"])
    chat_messages.append(to_send)
    # Emit the new chat message to all connected clients via WebSocket
    socketio.emit('chat_message', to_send, namespace='/twitch')

def start_listener():
    twitch = twitch_chat_irc.TwitchChatIRC()
    twitch.listen("heribio", on_message=twitch_message_received)

# Start the Twitch listener in a separate thread
twitch_thread = threading.Thread(target=start_listener)
twitch_thread.start()

@app.route("/")
def index():
    return ("OK", 200)

@socketio.on('connect', namespace='/twitch')
def handle_connect():
    emit('connected', {'data': 'Connected to Twitch WebSocket'})

@socketio.on('disconnect', namespace='/twitch')
def handle_disconnect():
    print('Disconnected from Twitch WebSocket')

@socketio.on('connect', namespace='/twitch')
def handle_chat_message(data):
    print("hello world")

@app.route("/twitch", methods=["GET"])
def twitch_chat_messages():
    return 


if __name__ == "__main__":
    socketio.run(app, host="localhost", port=6969)
