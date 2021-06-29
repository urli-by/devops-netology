import os

bash_command = ["cd ./", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
current_directory = os.getcwd()
counter = 0
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print('Modified:', current_directory + '\\' + prepare_result)
        counter += 1
    elif result.find('new') != -1:
        prepare_result = result.replace('\tnew file:   ', '')
        print('New file:', current_directory + '\\' + prepare_result)
        counter += 1
if counter == 0:
    print('nothing changed')

