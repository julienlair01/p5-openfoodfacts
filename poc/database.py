import queries
import mysql.connector
from mysql.connector import errorcode
from pprint import pprint

config = {
    'user': 'purbeurre',
    'password': '123456',
    'host': '127.0.0.1',
    'database': 'purbeurre',
    'raise_on_warnings': True
}

class Database():
    """
    docstring
    """
    def __init__(self):
        pass
    

    def connect_to_db(self):
        self.cnx = mysql.connector.connect(**config)
        self.cnx.raise_on_warnings = False
    

    def disconnect_from_db(self):
        self.cnx.close()


    def write_categories(self, categories):
        cursor = self.cnx.cursor()
        for i in range(len(categories['tags'])):
            if 'fr:' in categories['tags'][i]['id'] and categories['tags'][i]['known'] == 1:
                new_category = {
                    'off_id': categories['tags'][i]['id'],
                    'name': categories['tags'][i]['name']
                }
                cursor.execute(queries.insert_category, new_category)
            else:
                pass
        self.cnx.commit()
        cursor.close()

    def write_brands(self, brands):
        cursor = self.cnx.cursor()
        for i in range(len(brands['tags'])):
            new_brand = {
                'off_id': brands['tags'][i]['id'],
                'name': brands['tags'][i]['name']
            }
            cursor.execute(queries.insert_brand, new_brand)
        self.cnx.commit()
        cursor.close()

    def write_products(self, products):
        cursor = self.cnx.cursor()
        for i in range (len(products['products'])):
            new_product = {
                'barcode': products['products'][i]['code'],
                'name_fr': products['products'][i]['product_name_fr'],
                'generic_name': products['products'][i]['generic_name'],
                'nutrition_grade_fr': products['products'][i]['nutrition_grade_fr'],
                'off_url': products['products'][i]['url']
            }
            cursor.execute(queries.insert_product, new_product)
        self.cnx.commit()
        cursor.close()
        self.link_product_category(products)

    def link_product_category(self, products):
        pass



    def get_category_id(self, category_tag):
        query = ("SELECT id, name from Category "
                "WHERE off_id = %s")
        found_id = []
        cursor = self.cnx.cursor(dictionary=True)
        cursor.execute(query, (category_tag,)) # bof l'histoire du tuple...
        for row in cursor:
            found_id.append(row['id'])
        cursor.close()
        return found_id[0]
