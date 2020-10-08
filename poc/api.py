import requests

r = requests.get('https://fr.openfoodfacts.org/categories.json')

payload = {
            'action': 'process',
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': 'fr:pates-a-tartiner',
            'json': 'true'
            }

r = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=payload)
print(r.json())