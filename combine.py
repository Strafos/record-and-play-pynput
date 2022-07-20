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

    cur_end_id = cur[-1]["id"]
    for action in nxt:
        action["id"] = action["id"] + cur_end_id

for data in json_list:
    result += data

print("Writing combined recording to: " + output)
with open(output, 'w') as f:
    json.dump(result, f, indent=4)
