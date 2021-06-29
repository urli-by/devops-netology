import socket
import os

servers = ['drive.google.com', 'mail.google.com', 'google.com']
if os.path.exists('out.txt'):
    print('file exist')
    with open('out.txt', 'r') as f:
        for list_file in f:
            arr = {}
            row = list_file.split()
            key = row[0]
            value = row[1]
            arr[key] = value
            ip = socket.gethostbyname(arr[key])
            if ip != arr[key]:
                print('[ERROR]', arr[key],  'IP mismatch:', arr[value], '=>', ip)
    os.remove('out.txt')
else:
    print('file not exist, nothing to compare')

for server in servers:
    ip = socket.gethostbyname(server)
    print(server, ip)
    with open('out.txt', 'a') as f:
        print(server, ip, file=f)
