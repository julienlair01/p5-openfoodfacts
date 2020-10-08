import database
import requests
from pprint import pprint
import json

def get_json_from_off(url):
    r = requests.get(url)
    return r.json()

def get_products_from_off(category_tag):
    payload = {
            'action': 'process',
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category_tag,
            'json': 'true'
            }
    r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=payload)
    return r.json()


db = database.Database()
db.connect_to_db()
db.write_categories(get_json_from_off('https://fr.openfoodfacts.org/categories.json'))
print('Category table updated.')
db.write_products(get_products_from_off('fr:pates-a-tartiner'))
print('Product table updated.')
db.disconnect_from_db()

