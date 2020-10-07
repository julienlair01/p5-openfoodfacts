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
        self.add_category = ("INSERT INTO Category "
                "(id, off_id, name) "
                "VALUES (%(id)s, %(off_id)s, %(name)s)")
        self.add_product = ("INSERT INTO Product "
                "(id, barcode, name_fr, generic_name, brand, nutrition_grade_fr, off_url) " 
                "VALUES (0, %(barcode)s, %(name_fr)s, %(generic_name)s, %(brand)s, %(nutrition_grade_fr)s, %(off_url)s)")
    

    def connect_to_db(self):
        self.cnx = mysql.connector.connect(**config)
    

    def disconnect_from_db(self):
        self.cnx.close()


    def write_category(self, off_id, name):
        cursor = self.cnx.cursor()
        new_category = {
            'id': 0,
            'off_id': off_id,
            'name': name 
        }
        cursor.execute(self.add_category, new_category)
        self.cnx.commit()
        cursor.close()

    def write_products(self, products):
        cursor = self.cnx.cursor()
        for i in range (len(products)):
            cursor.execute(self.add_product, products[i])
        self.cnx.commit()
        cursor.close()


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
