import os

bash_command = ["cd ./", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
current_directory = os.getcwd()
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print('Modified:', current_directory + '\\' + prepare_result)
    elif result.find('new') != -1:
        prepare_result = result.replace('\tnew file:   ', '')
        print('New file:', current_directory + '\\' + prepare_result)
        exit('all done')
