import json
import yaml

with open('test.json', 'r') as json_file:
    js = json.load(json_file)
print(js)

with open('test.json', 'w') as new_f:
    new_f.write(json.dumps(js, indent=2))
