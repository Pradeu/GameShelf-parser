import json
import requests
import math

client_id = ''
authorization = ''

developers_count = requests.post('https://api.igdb.com/v4/companies/count',
                                 headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json',
                                          'Client-ID': f'{client_id}',
                                          'Authorization': f'{authorization}'},
                                 data='').json()

print(f'Количество компаний: {developers_count['count']}\n'
      f'Количество итераций запросов: {math.ceil(developers_count['count'] / 500)}')

s = 0
for i in range(math.ceil(developers_count['count'] / 500)):
    data = requests.post('https://api.igdb.com/v4/companies',
                         headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json',
                                  'Client-ID': f'{client_id}',
                                  'Authorization': f'{authorization}'},
                         data=f'fields name; sort id asc; limit 500; offset {s + 500 * i};').json()
    for item in data:
        s += 1
        genre = {'id': item['id'], 'name': str(item['name'])}
        print(json.dumps(item, indent=1))
        response = requests.post('http://localhost:5108/Developer', headers={'Content-Type': 'application/json'},
                                 json=genre)
        print(f'Номер разработчика:{s}')
        print(response)
    print(f'Итерация: {i+1}')
