#!/usr/bin/env python3
import os, sys
target_folder = sys.argv[1]
counter = 0
if os.path.isdir(target_folder + '//.git'):
    print('Next files were changed or created from last push')
else:
    print('folder not a git')
    exit()
bash_command = ["cd" + " " + target_folder, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print('Modified:', target_folder + '\\' + prepare_result)
        counter += 1
    elif result.find('new') != -1:
        prepare_result = result.replace('\tnew file:   ', '')
        print('New file:', target_folder + '\\' + prepare_result)
        counter += 1
if counter == 0:
    print('nothing changed')