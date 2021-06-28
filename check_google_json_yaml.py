import socket
import os
import json
import yaml


servers = ['drive.google.com', 'mail.google.com', 'google.com']

js_dict = {}
if os.path.exists('out.json'):
    print('file exist')
    with open('out.json', 'r') as f:
        js = json.load(f)
        yml = yaml.safe_load(f)
        for key in js:
            ip = socket.gethostbyname(key)
            if ip != js[key]:
                print('[ERROR]', key,  'IP mismatch:', js[key], '=>', ip)
    os.remove('out.json')
else:
    print('file not exist, nothing to compare')

for server in servers:
    ip = socket.gethostbyname(server)
    print(server, ip)
    js_dict[server] = ip
    with open('out.json', 'w') as file_json:
        file_json.write(json.dumps(js_dict, indent=2))
    with open('out.yaml', 'w') as file_yaml:
        file_yaml.write(yaml.safe_dump(js_dict, explicit_start=True, explicit_end=True))