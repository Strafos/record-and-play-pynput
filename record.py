from pynput import mouse
from pynput import keyboard
import time
import json
import sys

n = len(sys.argv)

if n < 2:
    exit("Takes a compulsory argument - name of recording")

if n == 2:
    name_of_recording = str(sys.argv[1])

print("Hold left click for more than 1 seconds (and then release) to end the recording for mouse and click 'esc' to end the recording for keyboard (both are needed to finish recording)")

storage = []
count = 0
id = 0
end = False

def on_press(key):
    global id
    id = id + 1
    try:
        json_object = {'id':id, 'action':'pressed_key', 'key':key.char, '_time': time.time()}
    except AttributeError:
        if key == keyboard.Key.f17:
            global end
            end = True
            with open(name_of_recording, 'w') as outfile:
                json.dump(storage, outfile)
            return False
        json_object = {'id':id, 'action':'pressed_key', 'key':str(key), '_time': time.time()}
    storage.append(json_object)

def on_release(key):
    global id
    id = id + 1
    try:
        json_object = {'id':id, 'action':'released_key', 'key':key.char, '_time': time.time()}
    except AttributeError:
        json_object = {'id':id, 'action':'released_key', 'key':str(key), '_time': time.time()}
    storage.append(json_object)

def on_move(x, y):
    global id
    id = id + 1

    global end
    if end:
        with open(name_of_recording, 'w') as outfile:
            json.dump(storage, outfile, indent=4)
        return False

    if len(storage) >= 1:
        if storage[-1]['action'] != "moved":
            json_object = {'id':id, 'action':'moved', 'x':x, 'y':y, '_time':time.time()}
            storage.append(json_object)
        # TODO should window be shorter?
        elif storage[-1]['action'] == "moved" and time.time() - storage[-1]['_time'] > 0.01:
            json_object = {'id':id, 'action':'moved', 'x':x, 'y':y, '_time':time.time()}
            storage.append(json_object)
    else:
        json_object = {'id':id, 'action':'moved', 'x':x, 'y':y, '_time':time.time()}
        storage.append(json_object)

def on_click(x, y, button, pressed):
    json_object = {'id':id, 'action':'pressed' if pressed else 'released', 'button':str(button), 'x':x, 'y':y, '_time':time.time()}
    storage.append(json_object)

def on_scroll(x, y, dx, dy):
    global id
    id = id + 1
    json_object = {'id':id, 'action': 'scroll', 'vertical_direction': int(dy), 'horizontal_direction': int(dx), 'x':x, 'y':y, '_time': time.time()}
    storage.append(json_object)
    global end
    end = True


# Collect events from keyboard until esc
# Collect events from mouse until scroll
keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

mouse_listener = mouse.Listener(
        on_click=on_click,
        on_scroll=on_scroll,
        on_move=on_move)

keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()
