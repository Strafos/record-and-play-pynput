from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
import time
import json
import sys

n = len(sys.argv)

pause = False
def on_press(key):
    try:
        k = key.char
    except AttributeError:
        if key == keyboard.Key.f18:
            global pause
            pause = not pause

keyboard_listener = keyboard.Listener(on_press=on_press)

m = mouse.Controller()
kb = keyboard.Controller()
keyboard_listener.start()

while True:
    print(pause)
    time.sleep(5)
    pass

