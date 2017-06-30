# The HTML parser
from bs4 import BeautifulSoup
# Fetching imdb's source
from urllib import request

# The model to save our data to
from ..models import Actor

men_list = 'http://www.imdb.com/list/ls050274118/'
women_list = 'http://www.imdb.com/list/ls000055475/'


# For Django's manage.py runscript
def run():

    def fetch_data_and_populate(imdb_list_url, gender):
        html = request.urlopen(imdb_list_url).read()
        soup = BeautifulSoup(html, 'html.parser')
        # A list with BeautifulSoup items to iterate over
        actor_items = soup.findAll('div', {'class': 'list_item'})
        new_actors = []
        for actor in actor_items:
            # Finds .list_item b a and its content
            name = actor.b.a.text
            # Finds .list_item's img tag and its source
            img_url = actor.img['src']
            # Create a new Actor object
            new_actors.append(Actor(name=name, img_url=img_url, gender=gender))

        # Save all models in 1 query instead of 100
        Actor.objects.bulk_create(new_actors)

    fetch_data_and_populate(men_list, 'M')
    fetch_data_and_populate(women_list, 'F')
