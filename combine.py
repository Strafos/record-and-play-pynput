import json
import sys

output = str(sys.argv[-1])

file_list = sys.argv[1:-1]
if len(file_list) < 2:
    exit("Need at least 2 input files")

result = []
json_list = []
for file_name in file_list:
    with open(file_name, 'r') as f:
        json_list.append(json.load(f))

for i in range(len(json_list) - 1):
    cur = json_list[i]
    nxt = json_list[i + 1]

    cur_end_time = cur[-1]["_time"]
    cur_end_id = cur[-1]["id"]
    nxt_start_time = nxt[0]["_time"]
    delta = nxt_start_time - cur_end_time

    for action in nxt:
        action["_time"] = action["_time"] - delta
        action["id"] = action["id"] + cur_end_id

for data in json_list:
    result += data

print("Writing combined recording to: " + output)
with open(output, 'w') as f:
    json.dump(result, f, indent=4)

