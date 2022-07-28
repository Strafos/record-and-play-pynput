from playback import playback

import json
import random
import sys
import time

# example json
# {
#   "programs": [
#     {
#       "files": ["alch"],
#       "iter": 1,
#       "delay": 0,
#       "init_pause": 1,
#       "nomove": 0,
#       "postsleep": 0,
#     },
#   ]
# }

if len(sys.argv) < 2:
  exit()

print(sys.argv)
program_file = str(sys.argv[-1])
if not program_file.startswith("programs/"):
    program_file = "programs/" + program_file

with open(program_file, 'r') as f:
  js = json.load(f)
  program = js["program"]

# TODO: need to handle loops recursively
# right now, we can do: A -> 10 * (B | C) -> D
# we can't do: 5 * (A -> 10 * (B | C) -> D)
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