import database
import requests
from pprint import pprint
import json

def get_categories_from_off():
    r = requests.get('https://fr.openfoodfacts.org/categories.json')
    return r.json()

def filter_categories(categories):
    filtered_categories = []
    for i in range (len(categories['tags'])):
        if "fr:" in categories['tags'][i]['id'] and categories['tags'][i]['known'] == 1:
            filtered_categories.append({
                'off_id': categories['tags'][i]['id'],
                'name': categories['tags'][i]['name']})
        else:
            pass
    print('Categories filtered, keeping FR and known categories only.')
    return filtered_categories

def get_products_from_off(category_tag):
    products = []
    payload = {
            'action': 'process',
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category_tag,
            'json': 'true'
            }
    r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=payload)
    products_raw = r.json()
    for i in range (len(products_raw['products'])):
        products.append({
            'barcode': products_raw['products'][i]['code'],
            'name_fr': products_raw['products'][i]['product_name_fr'],
            'generic_name': products_raw['products'][i]['generic_name'],
            'brand': trim_brands(products_raw['products'][i]['brands']),
            'nutrition_grade_fr': products_raw['products'][i]['nutrition_grade_fr'],
            'off_url': products_raw['products'][i]['url']
            })
    print("Products have been retrieved.")
    return(products)

def clean_product_categories():
    pass

def trim_brands(brands):
    return brands.split(',')[0]


db = database.Database()

raw_categories = get_categories_from_off()
filtered_categories = filter_categories(raw_categories)

db.connect_to_db()
for item in filtered_categories:
    db.write_category(item['off_id'], item['name'])

print('Category table updated.')

products = get_products_from_off('fr:pates-a-tartiner')
db.write_products(products)
print('Product table updated.')

db.disconnect_from_db()

