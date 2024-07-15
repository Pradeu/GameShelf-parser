import requests
import math
from datetime import datetime
from deep_translator import GoogleTranslator
import urllib.request

client_id = ''
authorization = ''

games_count = requests.post('https://api.igdb.com/v4/games/count',
                            headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json',
                                     'Client-ID': f'{client_id}',
                                     'Authorization': f'{authorization}'},
                            data='').json()

for i in range(math.ceil(games_count['count'] / 500)):
    data = requests.post('https://api.igdb.com/v4/games',
                         headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json',
                                  'Client-ID': f'{client_id}',
                                  'Authorization': f'{authorization}'},
                         data=f'fields name, summary, first_release_date,'
                              f'platforms, genres, involved_companies.company,'
                              f'involved_companies.developer, game_engines,'
                              f'cover.image_id; sort id asc; limit 500; offset {500 * i};').json()
    for item in data:
        companies = []
        game = dict(id=item['id'], name=item['name'],
                    description='',
                    releaseYear=int(), score=0, scoresCount=0, genreId=[],
                    platformId=[], engineId=[], developerId=[], usersId=[0])
        if 'platforms' in item:
            game['platformId'] = item['platforms']
        if 'first_release_date' in item:
            game['releaseYear'] = datetime.fromtimestamp(item['first_release_date']).year
        if 'genres' in item:
            game['genreId'] = item['genres']
        if 'summary' in item:
            game['description'] = GoogleTranslator(source='en', target='ru').translate(
                text=item['summary'].strip()).replace("\u200b", "")
        if 'involved_companies' in item:
            for developer in item['involved_companies']:
                if developer['developer']:
                    companies.append(developer['company'])
        game['developerId'] = companies
        if 'game_engines' in item:
            game['engineId'] = item['game_engines']
        if 'cover' in item:
            urllib.request.urlretrieve(
                f'https://images.igdb.com/igdb/image/upload/t_cover_big/{item['cover']['image_id']}.jpg',
                f"C:/Users/medov/Desktop/Диплом/Фронт/GameShelf/public/game_covers/{item['id']}.jpg")
        response = requests.post('http://localhost:5108/Game', headers={'Content-Type': 'application/json'}, json=game)
