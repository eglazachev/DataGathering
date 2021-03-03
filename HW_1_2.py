# 2. Изучить список открытых API. Найти среди них любое,
# требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

client_id = 'zVwObPOX5agaRQ'
secret_token = 'm96ATiJXxkxYdyj2VgSpn6Y6vaVujQ'
auth = requests.auth.HTTPBasicAuth(client_id, secret_token)

data = {'grant_type': 'password',
        'username': 'your_ugly_grandpa',
        'password': 'ESykF@-bx?XCE5m'}

headers = {'User-Agent': 'ugly_grandpa/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

me = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
with open('me.json', 'w') as f1:
    json.dump(me.json(), f1, sort_keys=True, indent=4)

preferences = requests.get('https://oauth.reddit.com/api/v1/me/prefs', headers=headers)
with open('my_preferences.json', 'w') as f2:
    json.dump(preferences.json(), f2, sort_keys=True, indent=4)

comments = requests.get('https://oauth.reddit.com/user/your_ugly_grandpa/overview', headers=headers)
with open('my_comments.json', 'w') as f3:
    json.dump(comments.json(), f3, sort_keys=True, indent=4)
