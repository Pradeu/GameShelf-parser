import json
import math
import requests

client_id = ''
authorization = ''

genres_count = requests.post('https://api.igdb.com/v4/genres/count',
                             headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json',
                                      'Client-ID': f'{client_id}',
                                      'Authorization': f'{authorization}'},
                     data='').json()

data = requests.post('https://api.igdb.com/v4/genres',
                     headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json',
                              'Client-ID': f'{client_id}',
                              'Authorization': f'{authorization}'},
                     data='fields name; sort id asc; limit 500;').json()

print(f'Количество платформ: {genres_count['count']}\n'
      f'Последний id: {data[len(data) - 1]['id']}\n'
      f'Количество итераций запросов: {math.ceil(genres_count['count'] / 500)}')

for item in data:
    genre = {'id': item['id'], 'name': str(item['name'])}
    response = requests.post('http://localhost:5108/Genre', headers={'Content-Type': 'application/json'}, json=genre).json()
    print(json.dumps(response, indent=1))
