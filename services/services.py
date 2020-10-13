# coding: utf-8
""" This module contains the Services classes.
    It manages everything related to the Products, 
    Categories and the Database connection. """

import category
import queries
import product

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
        self.filter_categories = [
            'Fromages',
            'Boissons',
            'Plats préparés',
            'Produits laitiers'
        ]

    def get_categories_from_off(self, db):
        """  
        Get all categories from Open Food Facts and keeps only
        the ones speciafied in filter_categories.

        db -- Database object
        """
        cat_json  = requests.get('https://fr.openfoodfacts.org/categories.json').json()
        print('OK...Categories retrieved from Open Food Facts.') 
        self.update_categories_in_db(db, cat_json)

    def update_categories_in_db(self, db, cat_json):
        """
        Writes new categories in the local database.
        db -- Database object
        cat_json -- json file containing categories to insert into local db
        """
        db.connect_to_db()
        with db.cnx.cursor() as cursor:
            for i in range(len(cat_json['tags'])):
                if cat_json['tags'][i]['name'] in self.filter_categories:
                    add_category = {
                        'off_id': cat_json['tags'][i]['id'],
                        'name': cat_json['tags'][i]['name']
                    }
                    cursor.execute(queries.insert_category, add_category)
        db.cnx.commit()
        print('OK...Inserted categories into db.')

    def get_categories_from_local(self, db):
        """
        Get categories from local db.
        Returns a list of Category objects.

        db -- Database object
        """
        db.connect_to_db()
        with db.cnx.cursor(named_tuple = True) as cursor:
            cursor.execute(queries.get_categories)
            for (id, name, off_id) in cursor:
                self.categories.append(category.Category(id, name, off_id))
        return self.categories


class ProductService():

    def __init__(self):
        pass

    def get_products(self, db, cat_service, category):
        """
        Checks if products already exist in the lcoal db for this category.
        If yes, returns a list of Product objects.
        If no, gets the product from OFF.
        """
        products = []
        with db.cnx.cursor(buffered=True) as cursor:
            cursor.execute(queries.get_products, {'cat_id': category.id})
            if cursor.rowcount > 0:
                for (id,) in cursor.fetchall():
                    products.append(product.Product(id = id))
            else:
                self.get_products_from_off(db, cat_service, category)
                return self.get_products(db, cat_service, category)
        return products

    def get_products_from_off(self, db, cat_service, category):
        """
        Retrieve the list of products of a given category, from
        the Open Food Facts API.

        db -- DatabaseService object
        cat_service -- CategoryService object
        category_id -- id of the category to get products from
        """
        page_size = 20
        # i = 0
        # skip = 0
        # while i >= 0:
        payload = {
                'action': 'process',
                'tagtype_0': 'countries',
                'tag_contains_0': 'contains',
                'tag_0': 'France',
                'tagtype_1': 'categories',
                'tag_contains_1': 'contains',
                'tag_1': category.name,
                'json': 'true',
                'page_size': page_size,
                # 'page': 1 + skip//page_size,
                'sort_by': 'unique_scans_n'
                }
        r = requests.get(url=URL_PRODUCTS, params=payload)
        clean_products = self.clean_products(r.json())
        self.add_product_to_db(clean_products, db, category.off_id)
            # skip += page_size
            # i = int(r.json()['count']) - skip

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

    def add_product_to_db(self, products, db, category):
        """
        Add products to the local database.
        Stores the relationship between product and category
        in the local database.
        Stores the relationship between product and brands in
        the local database

        products -- json of products to be added
        db -- DatabaseService object
        category -- str being the Open Food Facts id of a category
        """
        for i in range(len(products['products'])):
            add_product = {
                'barcode': products['products'][i]['code'],
                'name_fr': products['products'][i]['product_name_fr'],
                'generic_name': products['products'][i]['generic_name'],
                'nutrition_grade_fr': products['products'][i]['nutrition_grade_fr'],
                'url': products['products'][i]['url']
            }

            with db.cnx.cursor() as cursor:
                cursor.execute(queries.insert_product, add_product)  
                last_product_id = cursor.lastrowid
                add_product_category = {
                    'product_id': last_product_id,
                    'category': category,
                }
                cursor.execute(queries.insert_product_category, add_product_category)
                brands = products['products'][i]['brands'].split(',') 

                for j in range(len(brands)):
                    add_product_brand = {
                        'product_id': last_product_id,
                        'brand': brands[j]
                    }
                    cursor.execute(queries.insert_product_brand, add_product_brand)

        db.cnx.commit()


class DatabaseService():

    def __init__(self):
        self.config = DB_CONFIG
        self.connect_to_db()
        self.clear_tables()
        self.init_tables()
        self.disconnect_from_db()

    def __del__(self):
        self.disconnect_from_db()

    def connect_to_db(self):
        """
        Connects to the db, according to the config parameters given.
        config -- dict containing the configuration parameters (see constant)
        """
        self.cnx = mysql.connector.connect(**self.config)

    def disconnect_from_db(self):
        """
        Connects to the db, according to the config parameters given.
        config -- dict containing the configuration parameters (see constant)
        """
        self.cnx.close()

    def init_tables(self):
        """
        Initializes the tables, if they do not already exist.
        """
        with open(INIT_TABLES_FILE, 'r') as f:
            with self.cnx.cursor() as cursor:
                cursor.execute(f.read(), multi=True)

    def clear_tables(self):
        with open(CLEAR_DATA_FILE, 'r') as f:
            with self.cnx.cursor() as cursor:
                cursor.execute(f.read(), multi=True)
                self.cnx.commit()
        print('Tables dropped.')


class BrandService():
    
    def __init__(self, db):
        pass

    def get_brands_from_off(self, db):
        """  
        Get all brands from Open Food Facts.

        db -- Database object
        """
        brands_json  = requests.get('https://fr.openfoodfacts.org/brands.json').json()
        print('OK...Brands retrieved from Open Food Facts.') 
        self.update_brands_in_db(db, brands_json)

    def update_brands_in_db(self, db, brands_json):
        """
        Writes new categories in the local database.
        db -- Database object
        brands_json -- json file containing brands to insert into local db
        """
        db.connect_to_db()
        with db.cnx.cursor() as cursor:
            for i in range(len(brands_json['tags'])):
                add_brand = {
                    'off_id': brands_json['tags'][i]['id'],
                    'name': brands_json['tags'][i]['name']
                }
                cursor.execute(queries.insert_brand, add_brand)
        db.cnx.commit()
        print('OK...Inserted brands into db.')

