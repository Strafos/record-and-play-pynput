from pynput import mouse
from pynput import keyboard
import time
import json
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='path to output file')
args = parser.parse_args()
if not args.file.startswith("data/"):
    args.file = "data/" + args.file
print(args)

print("f17 to start recording; f18 to pause, f17 + move mouse to end recording.")

storage = []
count = 0
id = 0
last_warning_time = 0
start_recording = False
end_recording = False
pause_recording = False
start_time = 0
pause_time = 0
pause_position = (0, 0)
elapsed_pause_time = 0

m = mouse.Controller()

def log_elapsed(start, curr):
    delta = curr - start
    for i in range(1, 30):
        if delta > i * 60 and delta < (i * 60 + 1):
            print("Elapsed " + str(i) + " minutes")
            break

def on_press(key):
    global id, start_recording, pause_recording, end_recording, pause_time, elapsed_pause_time, pause_position

    if not start_recording:
        return True

    if key == keyboard.Key.f18:
        pause_recording = not pause_recording
        if pause_recording:
            print("Recording paused")
            pause_time = time.time()
            pause_position = m.position
        else:
            print("Recording unpaused")
            m.position = pause_position
            elapsed_pause_time = time.time() - pause_time

        return True

    if pause_recording:
        return True

    record_time = time.time() - elapsed_pause_time
    log_elapsed(start_time, record_time)
    delay = record_time - storage[-1]['_time']

    id = id + 1
    try:
        json_object = {'id':id, 'action':'pressed_key', 'key':key.char, '_time': record_time, 'delay': delay}
    except AttributeError:
        if key == keyboard.Key.f17:
            end_recording = True
            print("Recording stopped at " + str(time.time()))
            print("Elapsed time: " + str((time.time() - start_time)/60) + " minutes")
            print("Elapsed pause time: " + str(elapsed_pause_time/60) + " minutes")
            with open(args.file, 'w') as outfile:
                json.dump(storage[1:], outfile, indent=4)
            return False
        json_object = {'id':id, 'action':'pressed_key', 'key':str(key), '_time': record_time, 'delay': delay}
    storage.append(json_object)

def on_release(key):
    global id, start_recording, pause_recording, start_time

    if not start_recording:
        if key == keyboard.Key.f17:
            start_time = time.time()
            print("Recording started at " + str(start_time))
            start_recording = True

            json_object = {'id':id, '_time': start_time, 'action': 'dummy_val'}
            storage.append(json_object)
        return True

    if pause_recording:
        return True

    record_time = time.time() - elapsed_pause_time
    delay = record_time - storage[-1]['_time']
    log_elapsed(start_time, record_time)

    id = id + 1
    try:
        json_object = {'id':id, 'action':'released_key', 'key':key.char, '_time': record_time, 'delay': delay}
    except AttributeError:
        json_object = {'id':id, 'action':'released_key', 'key':str(key), '_time': record_time, 'delay': delay}
    storage.append(json_object)

def on_move(x, y):
    global id, start_recording, pause_recording, end_recording, last_warning_time
    if not start_recording:
        curr = time.time()
        if curr - last_warning_time > 1:
             print("Recording hasn't started!")
             last_warning_time = curr
        return True

    if pause_recording:
        return True

    if end_recording:
        return False

    id = id + 1
    record_time = time.time() - elapsed_pause_time
    delay = record_time - storage[-1]['_time']
    log_elapsed(start_time, record_time)

    if len(storage) >= 1:
        if storage[-1]['action'] != "moved":
            json_object = {'id':id, 'action':'moved', 'x':x, 'y':y, '_time':record_time, 'delay': delay}
            storage.append(json_object)
        elif record_time - storage[-1]['_time'] > 0.005:
            json_object = {'id':id, 'action':'moved', 'x':x, 'y':y, '_time':record_time, 'delay': delay}
            storage.append(json_object)
    else:
        json_object = {'id':id, 'action':'moved', 'x':x, 'y':y, '_time':record_time}
        storage.append(json_object)

def on_click(x, y, button, pressed):
    global start_recording, pause_recording, id
    if not start_recording or pause_recording:
        return True

    id = id + 1
    record_time = time.time() - elapsed_pause_time
    log_elapsed(start_time, record_time)
    delay = record_time - storage[-1]['_time']

    json_object = {'id':id, 'action':'pressed' if pressed else 'released', 'button':str(button), 'x':x, 'y':y, '_time':record_time, 'delay': delay}
    storage.append(json_object)

keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)

keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()
