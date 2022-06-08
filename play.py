from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
import time
import json
import sys

n = len(sys.argv)

if n == 2:
    name_of_recording = str(sys.argv[1])
    number_of_plays = 1
else:
    name_of_recording = str(sys.argv[1])
    number_of_plays = int(sys.argv[2])

with open(name_of_recording) as json_file:
    data = json.load(json_file)

# f18 to pause
pause = False
def on_press(key):
    try:
        k = key.char
    except AttributeError:
        if key == keyboard.Key.f18:
            global pause
            pause = not pause

keyboard_listener = keyboard.Listener(on_press=on_press)

special_keys = {"Key.esc": Key.esc, "Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}

m = mouse.Controller()
kb = keyboard.Controller()
keyboard_listener.start()

count = len(data)

for loop in range(number_of_plays):
    index = 0
    while index < count - 1:
        if pause:
            continue

        obj = data[index]

        id, action, _time = obj['id'], obj['action'], obj['_time']
        try:
            next_movement = data[index+1]['_time']
            pause_time = next_movement - _time
        except IndexError as e:
            break

        print("id: {0}, pause_time: {1}".format(id, pause_time))
        if action == "pressed_key" or action == "released_key":
            key = obj['key'] if 'Key.' not in obj['key'] else special_keys[obj['key']]
            # print("id: {0}, action: {1}, time: {2}, key: {3}".format(id, action, _time, str(key)))
            if action == "pressed_key":
                kb.press(key)
            elif action == "released_key":
                kb.release(key)
        else:
            x, y = obj['x'], obj['y']
            # print("id: {0}, x: {1}, y: {2}, action: {3}, time: {4}".format(id, x, y, action, _time))
            m.position = (x, y)

            if action == "pressed":
                mouse.press(mouse.Button.left if obj['button'] == "Button.left" else mouse.Button.right)
#                time.sleep(.15)
            elif action == "released":
                mouse.release(mouse.Button.left if obj['button'] == "Button.left" else mouse.Button.right)
#                time.sleep(.15)

        index += 1
        time.sleep(pause_time)

