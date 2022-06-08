from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import time
import json
import sys

n = len(sys.argv)

delay = .3
if n == 2:
    name_of_recording = str(sys.argv[1])
    number_of_plays = 1
elif n == 4:
    name_of_recording = str(sys.argv[1])
    number_of_plays = int(sys.argv[2])
    delay = float(sys.argv[3])
elif n == 3:
    name_of_recording = str(sys.argv[1])
    number_of_plays = int(sys.argv[2])

print(delay)

with open(name_of_recording) as json_file:
    data = json.load(json_file)

special_keys = {"Key.esc": Key.esc, "Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}

mouse = MouseController()
keyboard = KeyboardController()

for loop in range(number_of_plays):
    for index, obj in enumerate(data):
        id, action, _time = obj['id'], obj['action'], obj['_time']
        try:
            next_movement = data[index+1]['_time']
            pause_time = next_movement - _time
        except IndexError as e:
            pause_time = 1

        if action == "pressed_key" or action == "released_key":
            if obj['key'] == "null":
                continue
            key = obj['key'] if 'Key.' not in obj['key'] else special_keys[obj['key']]
            if action == "pressed_key":
                keyboard.press(key)
            else:
                keyboard.release(key)


        else:
            move_for_scroll = True
            x, y = obj['x'], obj['y']
            if action == "scroll" and index > 0 and (data[index - 1]['action'] == "pressed" or data[index - 1]['action'] == "released"):
                if x == data[index - 1]['x'] and y == data[index - 1]['y']:
                    move_for_scroll = False
            mouse.position = (x, y)

            if action == "pressed":
                time.sleep(delay)
                mouse.press(Button.left if obj['button'] == "Button.left" else Button.right)
            elif action == "released":
                mouse.release(Button.left if obj['button'] == "Button.left" else Button.right)
            elif action == "scroll":
                horizontal_direction, vertical_direction = obj['horizontal_direction'], obj['vertical_direction']
                mouse.scroll(horizontal_direction, vertical_direction)

        time.sleep(pause_time)
