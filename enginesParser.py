import json
import math
import requests

client_id = ''
authorization = ''

engines_count = requests.post('https://api.igdb.com/v4/game_engines/count',
                              headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json',
                                       'Client-ID': f'{client_id}',
                                       'Authorization': f'{authorization}'},
                              data='').json()

print(f'Количество компаний: {engines_count['count']}\n'
      f'Количество итераций запросов: {math.ceil(engines_count['count'] / 500)}')

for i in range(math.ceil(engines_count['count'] / 500)):
    data = requests.post('https://api.igdb.com/v4/game_engines',
                         headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json',
                                  'Client-ID': f'{client_id}',
                                  'Authorization': f'{authorization}'},
                         data=f'fields name; sort id asc; limit 500; offset {500 * i};').json()
    for item in data:
        engine = {'id': item['id'], 'name': str(item['name'])}
        response = requests.post('http://localhost:5108/Engine', headers={'Content-Type': 'application/json'},
                                 json=engine).json()
        print(json.dumps(response, indent=1))

    print(f'Итерация: {i + 1}')
