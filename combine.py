import json
import sys

if len(sys.argv) != 4:
    exit("Input two data files and output file name")

output = str(sys.argv[3])

f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'r')

with open(sys.argv[1]) as f:
    data1 = json.load(f)

with open(sys.argv[2]) as f:
    data2 = json.load(f)

data1_end = data1[-1]["_time"]
data2_start = data2[0]["_time"]
data1_end_id = data1[-1]["id"]

# Include a second of delay when combining
delta = data2_start - data1_end - 1

for action in data2:
    action["_time"] = action["_time"] - delta
    action["id"] = action["id"] + data1_end_id

with open(output, 'w') as f:
    json.dump(data1 + data2, f, indent=4)
