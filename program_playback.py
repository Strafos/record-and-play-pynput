from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse

import argparse
import json
import random
import sys
import time

# new format
# program = {
#   "type": "actions"|"files"|"program"
#   files OR actions OR programs
#   "files": [...],
#   "actions": [...],
#   "programs": [
#     {
#       "files": ["alch"],
#       "iter": 1,
#       "delay": 0,
#       "init_pause": 1,
#       "nomove": 0,
#       "postsleep": 0,
#     },
#   ],
#   "iter": 1,
#   "delay": 0,
#   "init_pause": 1,
#   "nomove": 0,
#   "postsleep": 0,
# }

pause = False
offset = 0

# f17 adds offset
# f18 to pause
def on_press(key):
    try:
        k = key.char
    except AttributeError:
        if key == keyboard.Key.f18:
            global pause
            pause = not pause
            if pause:
                print("Playback paused")
            else:
                print("Playback resumed")
        if key == keyboard.Key.f17:
            global offset
            offset = .1
            print("Add .1s offset")

keyboard_listener = keyboard.Listener(on_press=on_press)
m = mouse.Controller()
kb = keyboard.Controller()
keyboard_listener.start()

def play_actions(data, delay, nomove):
    global pause, offset, m, kb

    special_keys = {"Key.esc": Key.esc, "Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}

    index = 0
    while index < len(data) - 1:
        if pause:
            continue
        if offset != 0:
            time.sleep(offset)
            offset = 0

        obj = data[index]
        id, action, _time = obj['id'], obj['action'], obj['_time']

        # TODO: delay results in different playback, why?
        base_pause_time = obj['delay']
        try:
            next_movement = data[index+1]['_time']
            pause_time = max(next_movement - _time, 0)
        except IndexError as e:
            break

        # if base_pause_time != pause_time:
        #     print(id, pause_time, base_pause_time)

        random_pause = max(0, random.randint(delay - 10, delay + 10)/100 if delay != 0 else random.randint(0, 8)/100)
        if action == "pressed_key" or action == "released_key":
            key = obj['key'] if 'Key.' not in obj['key'] else special_keys[obj['key']]
            if action == "pressed_key":
                kb.press(key)
            elif action == "released_key":
                kb.release(key)
        else:
            x, y = obj['x'], obj['y']
            if not nomove:
                m.position = (x, y)

            if action == "pressed":
                time.sleep(random_pause)
                m.press(mouse.Button.left if obj['button'] == "Button.left" else mouse.Button.right)
            elif action == "released":
                m.release(mouse.Button.left if obj['button'] == "Button.left" else mouse.Button.right)

        index += 1
        if pause_time > 0:
            time.sleep(pause_time)

def read_file(filepath):
  with open(filepath, 'r') as f:
    return json.load(f)

def handle_programs(programs, delay):
    for program in programs:
        handle_program(program, default_delay=delay)

def play_files(files, delay, nomove):
    file = random.choice(files)
    data = read_file(file)
    length = (data[-1]["_time"] - data[0]["_time"])/60
    print(f"Playing file '{file}', len={length}, delay={delay}, nomove={nomove}")
    play_actions(data, delay, nomove)

def handle_program(program, default_delay=0):
    global pause
    pause = program.get("init_pause", False)
    iter = program.get("iter", 1)
    delay = program.get("delay", default_delay)
    nomove = program.get("nomove", False)
    postsleep = program.get("postsleep", 0)

    for _ in range(iter):
        if "programs" in program:
            print("Handle program: ")
            print(program)
            handle_programs(program["programs"], delay)
        elif "actions" in program:
            play_actions(program["actions"], delay, nomove)
        elif "files" in program:
            play_files(program["files"], delay, nomove)

    if postsleep:
        time.sleep(postsleep)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='path to the input file')
    parser.add_argument('--iter', type=int, help='number of iterations', default=1)
    parser.add_argument('--delay', type=int, help='delay on click in ms', default=0)
    parser.add_argument('--pause', action='store_true', help='pause playback initially')
    parser.add_argument('--nomove', action='store_true', help='pause playback initially')
    args = parser.parse_args()
    print(args)

    time.sleep(2)
    js = read_file(args.file)

    if isinstance(js, list):
        # Legacy format, treat as actions
        program = {
            "actions": js,
            "iter": args.iter,
            "delay": args.delay,
            "init_pause": args.pause,
            "nomove": args.nomove,
        }
        handle_program(program, args.delay)
    elif isinstance(js, dict):
        handle_program(js, args.delay)
    else:
      raise Exception("")
