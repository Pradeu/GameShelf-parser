import json
import math
import requests

client_id = ''
authorization = ''

platforms_count = requests.post('https://api.igdb.com/v4/platforms/count',
                                headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json',
                                         'Client-ID': f'{client_id}',
                                         'Authorization': f'{authorization}'},
                              data='').json()

data = requests.post('https://api.igdb.com/v4/platforms',
                     headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json',
                              'Client-ID': f'{client_id}',
                              'Authorization': f'{authorization}'},
                     data='fields name; sort id asc; limit 500;').json()

print(f'Количество платформ: {platforms_count['count']}\n'
      f'Последний id: {data[0]['id']}\n'
      f'Количество итераций запросов: {math.ceil(platforms_count['count'] / 500)}')

for item in data:
    platform = {'id': item['id'], 'name': str(item['name'])}
    response = requests.post('http://localhost:5108/Platform', headers={'Content-Type': 'application/json'}, json=platform).json()
    print(json.dumps(response, indent=1))
