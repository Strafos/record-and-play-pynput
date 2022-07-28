from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
import random
import time
import json
import argparse

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

def playback(file, delay, init_pause, nomove):
    global pause, offset
    pause = init_pause

    if not file.startswith("data/"):
        file = "data/" + file
    with open(file) as f:
        data = json.load(f)

    special_keys = {"Key.esc": Key.esc, "Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space}

    keyboard_listener = keyboard.Listener(on_press=on_press)
    m = mouse.Controller()
    kb = keyboard.Controller()
    keyboard_listener.start()

    print(file + " length: " + str((data[-1]["_time"] - data[0]["_time"])/60) + " mins")

    index = 0
    while index < len(data) - 1:
        if pause:
            continue
        if offset != 0:
            time.sleep(offset)
            offset = 0

        obj = data[index]
        id, action, _time = obj['id'], obj['action'], obj['_time']

        # pause_time = obj['delay']
        # Delete this after testing that the delay format works
        try:
            next_movement = data[index+1]['_time']
            pause_time = max(next_movement - _time, 0)
        except IndexError as e:
            break

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

    for i in range(args.iter):
        print("Iter: " + str(i + 1))
        playback(args.file, args.delay, args.pause, args.nomove)