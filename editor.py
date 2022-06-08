import json

with open('blast_furn') as f:
    data = json.load(f)
    
for i in data:
    print(i)
