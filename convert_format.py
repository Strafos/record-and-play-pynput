import sys
import json

filename = sys.argv[-1]

with open(filename, 'r') as f:
    data = json.load(f)

i = 0
while i < len(data) - 1:
    cur = data[i]
    nxt = data[i + 1]
    delay = nxt['_time'] - cur['_time']
    data[i]['delay'] = delay
    i += 1

data[-1]['delay'] = 0

with open(filename, 'w') as f:
    json.dump(data, f, indent=4)
