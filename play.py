from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
import random
import time
import json
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='path to the input file')
parser.add_argument('--iter', type=int, help='number of iterations', default=1)
parser.add_argument('--delay', type=int, help='delay on click in ms', default=0)
parser.add_argument('--pause', action='store_true', help='pause playback initially')
args = parser.parse_args()
print(args)

offset = 0

with open(args.file) as f:
    data = json.load(f)

# f18 to pause
pause = args.pause
def on_press(key):
    try:
        k = key.char
    except AttributeError:
        if key == keyboard.Key.f18:
            global pause
            pause = not pause
        if key == keyboard.Key.f17:
            global offset
            offset = .1

special_keys = {"Key.esc": Key.esc, "Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}

keyboard_listener = keyboard.Listener(on_press=on_press)
m = mouse.Controller()
kb = keyboard.Controller()
keyboard_listener.start()

print("Record length: " + str((data[-1]["_time"] - data[0]["_time"])/60) + " mins")
time.sleep(2)

for loop in range(args.iter):
    print("Iter: " + str(loop + 1))

    index = 0
    while index < len(data) - 1:
        if pause:
            continue
        if offset != 0:
            time.sleep(offset)
            offset = 0

        obj = data[index]

        id, action, _time = obj['id'], obj['action'], obj['_time']
        pause_time = obj['delay']
        # # Delete this after testing that the delay format works
        # try:
        #     next_movement = data[index+1]['_time']
        #     pause_time = next_movement - _time
        # except IndexError as e:
        #     break

        if action == "pressed_key" or action == "released_key":
            key = obj['key'] if 'Key.' not in obj['key'] else special_keys[obj['key']]
            if action == "pressed_key":
                kb.press(key)
            elif action == "released_key":
                kb.release(key)
        else:
            x, y = obj['x'], obj['y']
            m.position = (x, y)

            random_pause = random.randint(args.delay - 10, args.delay + 10)/100 if args.delay != 0 else random.randint(0, 5)/100
            if action == "pressed":
                time.sleep(random_pause)
                m.press(mouse.Button.left if obj['button'] == "Button.left" else mouse.Button.right)
            elif action == "released":
                m.release(mouse.Button.left if obj['button'] == "Button.left" else mouse.Button.right)

        index += 1
        if pause_time > 0:
            time.sleep(pause_time)

