# coding: utf-8
""" This module contains the Services classes.
    It manages everything related to the Products, 
    Categories and the Database connection. """

import category
import queries

from pprint import pprint
import mysql.connector
import requests

DB_CONFIG = {
                'user': 'purbeurre',
                'password': '123456',
                'host': '127.0.0.1',
                'database': 'purbeurre'
                }
INIT_TABLES_FILE = '/Users/julienlair/Formation_Python/projet5/app/create_tables.sql'
CLEAR_DATA_FILE = '/Users/julienlair/Formation_Python/projet5/app/drop_tables.sql'
URL_PRODUCTS = 'https://fr.openfoodfacts.org/cgi/search.pl'



class CategoryService():
    
    def __init__(self, db):
        self.categories = []
        self.categories_local = []
        # self.get_categories_from_off(db)
        # self.update_categories_in_db(db)
    
    def get_categories_from_off(self, db):
        """  
        Get all categories from Open Food Facts and keeps only
        the FR and known categories.
        Returns the results as a list of Category objects.
        """
        cat_json  = requests.get('https://fr.openfoodfacts.org/categories.json').json()
        print('OK...Categories retrieved from Open Food Facts.') 

        for i in range(len(cat_json['tags'])):
            if 'fr:' in cat_json['tags'][i]['id'] and cat_json['tags'][i]['known'] == 1:
                self.categories.append(category.Category(off_id = cat_json['tags'][i]['id'], name = cat_json['tags'][i]['name']))
            else:
                pass
        
        print('List of Category objects created.') 

    def update_categories_in_db(self, db):
        """
        Writes new categories in the local database.
        categories -- list of Category objects
        """
        db.connect_to_db()
        for i in range(len(self.categories)):
            add_category = {
                    'off_id': self.categories[i].off_id,
                    'name': self.categories[i].name
                }
            with db.cnx.cursor() as cursor:
                cursor.execute(queries.insert_category, add_category)
                db.cnx.commit()
        print('Inserted categories into db.')

    def get_categories_from_local(self, db):
        db.connect_to_db()

        with db.cnx.cursor(named_tuple = True) as cursor:
            cursor.execute(queries.get_categories)
            for (id, name) in cursor:
                self.categories_local.append(category.Category(id, name))
        return self.categories_local


class ProductService():

    def __init__(self):
        pass

    def get_products_from_off(self, category_id, db, cat_service):
        """
        Retrieve the list of products of a given category, from
        the Open Food Facts API.

        category_tag -- category tag from the Category table
        """
        products = {}
        page_size = 50
        i = 0
        skip = 0

        while i >= 0:
            payload = {
                    'action': 'process',
                    'tagtype_0': 'categories',
                    'tag_contains_0': 'contains',
                    'tag_0': cat_service.get_category_off_id(),
                    'json': 'true',
                    'page_size': page_size,
                    'page': 1 + skip//page_size
                    }
            r = requests.get(url=URL_PRODUCTS, params=payload)
            products = self.clean_products(r.json())
            self.add_product_to_db(products, db, category)
            print('Products inserted, page', 1 + skip//page_size)
            skip += page_size
            i = int(r.json()['count']) - skip

    def add_product_to_db(self, products, db, category):
        """
        Add products to the local database.
        Stores the relationship between product and category
        in the local database.

        products -- dict of products to be added
        db -- DatabaseService object
        category -- str being the Open Food Facts id of a category
        """
        for i in range(len(products['products'])):
            add_product = {
                'barcode': products['products'][i]['code'],
                'name_fr': products['products'][i]['product_name_fr'],
                'generic_name': products['products'][i]['generic_name'],
                'nutrition_grade_fr': products['products'][i]['nutrition_grade_fr'],
                'off_url': products['products'][i]['url']
            }

            with db.cnx.cursor() as cursor:
                cursor.execute(queries.insert_product, add_product)  
                add_product_category = {
                    'product_id': cursor.lastrowid,
                    'category': category,
                }
                cursor.execute(queries.insert_product_category, add_product_category) 
                db.cnx.commit()
                
        print('Inserted products into db.')
        print('Inserted product categories into db.')

    def clean_products(self, products):
        """
        Method to clean products which do not have specific keys,
        contained in keys[].
        """
        keys = ['code', 'product_name_fr', 'generic_name', 'nutrition_grade_fr', 'url']
        for i in range(len(products['products'])):
            for j in range(len(keys)):
                try:
                    buf = products['products'][i][keys[j]]
                except KeyError:
                    products['products'][i][keys[j]] = ''
        return products
        pass


class DatabaseService():

    def __init__(self):
        self.config = DB_CONFIG
        self.connect_to_db()
        # self.clear_tables()
        self.init_tables()

    def __del__(self):
        self.disconnect_from_db()

    def connect_to_db(self):
        """
        Connects to the db, according to the config parameters given.
        config -- dict containing the configuration parameters (see constant)
        """
        self.cnx = mysql.connector.connect(**self.config)
        # print('DB connection status:', self.cnx.is_connected())

    def disconnect_from_db(self):
        """
        Connects to the db, according to the config parameters given.
        config -- dict containing the configuration parameters (see constant)
        """
        self.cnx.close()
        print('DB connection status:', self.cnx.is_connected())

    def init_tables(self):
        """
        Initializes the tables, if they do not already exist.
        """
        with open(INIT_TABLES_FILE, 'r') as f:
            with self.cnx.cursor() as cursor:
                cursor.execute(f.read(), multi=True)
        print('Tables created.')
        print('DB connection status:', self.cnx.is_connected())

    def clear_tables(self):
        # self.connect_to_db()
        with open(CLEAR_DATA_FILE, 'r') as f:
            with self.cnx.cursor() as cursor:
                cursor.execute(f.read(), multi=True)
                self.cnx.commit()
        print('Tables dropped.')
        print('DB connection status:', self.cnx.is_connected())

