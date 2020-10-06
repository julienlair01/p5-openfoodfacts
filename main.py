import database
import json
from pprint import pprint

def read_categories_from_json():
    with open('categories.json', 'r') as f:
        categories = json.load(f)
    return categories

def filter_fr_categories(categories):
    fr_categories = []
    for i in range (len(categories['tags'])):
        if "fr:" in categories['tags'][i]['id']:
            fr_categories.append({'off_id': categories['tags'][i]['id'], 'name': categories['tags'][i]['name']})
        else:
            pass
    return fr_categories


db = database.Database()

raw_categories = read_categories_from_json()
clean_fr_categories = filter_fr_categories(raw_categories)

for item in clean_fr_categories:
    db.write_category(item['off_id'], item['name'])


