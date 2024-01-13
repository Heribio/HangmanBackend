import logging
import requests
from flask import Flask, request

from twitch_chat_irc import twitch_chat_irc

app = Flask(__name__)

LOG = logging.getLogger(__name__)

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
    #print content and author
    print(to_send["displayName"], to_send["content"])
    response = requests.post("http://localhost:5000/twitch", json=to_send)
    if response.status_code != 200:
        LOG.error(f"Failed to publish chat: {response.text}")

def start_listener():
    twitch = twitch_chat_irc.TwitchChatIRC()
    twitch.listen("heribio", on_message=twitch_message_received)

#if content is one letter long and isnt a number
def letter_sent(content):
    if content.lower().isalpha() and len(content) == 1:
        to_send = {
            "type": "letter_sent",
            "content": content.lower(),
        }
        response = requests.post("http://localhost:5000/twitch", json=to_send)
        print(to_send["content"])
        print("Sent letter")
        if response.status_code != 200:
            app.logger.error(f"Failed to publish chat: {response.text}")

if __name__ == "__main__":
    start_listener()
    print("Python script started listening...")
    print("Press Ctrl+C to stop the script.")
    while True:
        pass
