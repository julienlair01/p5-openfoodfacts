import database
import json
from pprint import pprint

def read_categories_from_json():
    with open('categories.json', 'r') as f:
        categories = json.load(f)
    print('Categories extracted from json.')
    return categories

def filter_categories(categories):
    filtered_categories = []
    for i in range (len(categories['tags'])):
        if "fr:" in categories['tags'][i]['id']:
            filtered_categories.append({'off_id': categories['tags'][i]['id'], 'name': categories['tags'][i]['name'][3:]})
        else:
            pass
    print('Categories filtered, keeping FR only.')
    return filtered_categories

db = database.Database()

raw_categories = read_categories_from_json()
filtered_categories = filter_categories(raw_categories)

db.connect_to_db()

for item in filtered_categories:
    db.write_category(item['off_id'], item['name'])

db.disconnect_from_db()

print('Category table updated.')

