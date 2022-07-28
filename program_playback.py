from playback import playback

import json
import random
import sys
import time

if len(sys.argv) < 2:
  exit()

print(sys.argv)
program_file = str(sys.argv[-1])
if not program_file.startswith("programs/"):
    program_file = "programs/" + program_file

with open(program_file, 'r') as f:
  js = json.load(f)
  program = js["program"]

for obj in program:
    files = obj.get("files")
    iter = obj.get("iter", 1)
    delay = obj.get("delay", 0)
    pause = obj.get("init_pause", False)
    nomove = obj.get("nomove", False)
    postsleep = obj.get("postsleep", 0)

    for i in range(iter):
      file = random.choice(files)
      print(f"Iter {i} - {file}")

      playback(file, delay, pause, nomove)
      if postsleep:
        time.sleep(postsleep)