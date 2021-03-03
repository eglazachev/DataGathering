# 1. Посмотреть документацию к API GitHub, разобраться как вывести список
# репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json


user_name = 'eglazachev'
curr_user = input('Type a username to get it public repos\n'
                  'Or just press enter to skip ')
if curr_user != '':
    user_name = curr_user
url = f"https://api.github.com/users/{user_name}/repos"
headers = {
    "Accept": "application/vnd.github.v3+json"
}
r = requests.get(url, headers=headers)
if r.ok:
    print('success')
    print(r.status_code)
    with open('repos.json', 'w') as f:
        json.dump(r.json(), f, sort_keys=True, indent=4)
