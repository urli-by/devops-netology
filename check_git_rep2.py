#!/usr/bin/env python3
import os, sys
repo_dir = sys.argv[1]
bash_command = ["cd" + " " + repo_dir, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', repo_dir + "/")
        print(prepare_result)