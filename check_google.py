import socket
import os

servers = ['drive.google.com', 'mail.google.com', 'google.com']
if os.path.exists('out.txt'):
    print('file exist')
    with open('out.txt', 'r') as f:
        for list_file in f:
            k, v = list_file.strip().split()
            ip = socket.gethostbyname(k)
            if ip != v:
                print('[ERROR]', k,  'IP mismatch:', v, '=>', ip)
    os.remove('out.txt')
else:
    print('file not exist, nothing to compare')

for server in servers:
    ip = socket.gethostbyname(server)
    print(server, ip)
    with open('out.txt', 'a') as f:
        print(server, ip, file=f)
