import subprocess
import os

servers = ['drive.google.com', 'mail.google.com', 'google.com']


for server in servers:
    ping = subprocess.Popen(["ping", "-n", "1", server], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    data = str(ping.communicate())
    list = []
    for line in data.split():
        list.append(line)
    formatted_list = list[1:3]
#    print(formatted_list)
    with open('out.txt', 'a') as f:
        print(list[1:3], file=f)
#    print(list[1:3])
with open('out.txt', 'r') as file:
    for i in file:
        for k in formatted_list:
            if i == k:
                print(equal)
            else:
                print('[ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>')
os.remove('out.txt')


