from bs4 import BeautifulSoup
from urllib import request
import json

men_list = 'http://www.imdb.com/list/ls050274118/'
women_list = 'http://www.imdb.com/list/ls000055475/'

def fetch_actors(list):
    html = request.urlopen(list).read()
    soup = BeautifulSoup(html, 'html.parser')
    actor_items =  soup.findAll('div', {'class': 'list_item'})

    result = []
    for actor in actor_items:
        name = actor.b.a.text
        img_url = actor.img['src']
        result.append({ 'name': name, 'url': img_url })

    return result

result = { 'men': fetch_actors(men_list), 'women': fetch_actors(women_list) }

with open('actors.json', 'w') as file:
    json.dump(result, file)
    print('Done!')
