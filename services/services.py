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


class CategoryService():
    
    def __init__(self, db):
        self.categories = []
        self.db = db
        self.filter_categories = [
            'Fromages',
            'Boissons',
            'Plats préparés',
            'Produits laitiers'
        ]
        self.load_categories(db)

    def load_categories(self, db):
        """
        Get categories, from local db if they exist,
        or from Open Food Facts if they do not.
        List Caterogy object in categories[]
        
        db -- DatabaseService object
        """
        self.load_categories_from_local(db)
        if self.categories == []:
            self.load_categories_from_off(db)
            self.load_categories_from_local(db)
        else:
            print('OK...Categories already exist locally.') 

    def load_categories_from_off(self, db):
        """  
        Get all categories from Open Food Facts and keeps only
        the ones speciafied in filter_categories.

        db -- Database object
        """
        cat_json  = requests.get('https://fr.openfoodfacts.org/categories.json').json()
        print('OK...Categories retrieved from Open Food Facts.') 
        self.update_categories_in_db(db, cat_json)

    def load_categories_from_local(self, db):
        """
        Get categories from local db.
        Returns a list of Category objects.

        db -- Database object
        """
        db.connect_to_db()
        with db.cnx.cursor(named_tuple = True, buffered = True) as cursor:
            cursor.execute(queries.get_categories)
            if cursor.rowcount > 0:
                for (id, name, off_id) in cursor:
                    self.categories.append(category.Category(id, name, off_id))
        db.disconnect_from_db()

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


class BrandService():
    
    def __init__(self, db):
        self.get_brands(db)

    def get_brands(self, db):
        """
        Get brands, from local db if they exist,
        or from Open Food Facts if they do not.

        db -- DatabaseService object
        """
        if self.count_brands_in_local(db) == 0:
            self.get_brands_from_off(db)
        else:
            print('OK...Brands already exist locally.') 

    def count_brands_in_local(self, db):
        """  
        Counts brands in local db.

        db -- Database object
        """
        db.connect_to_db()
        with db.cnx.cursor(named_tuple = True, buffered = True) as cursor:
            cursor.execute(queries.count_brands)
            (total,) = cursor.fetchone()
            return total
        db.disconnect_from_db()

    def get_brands_from_off(self, db):
            """  
            Gets all brands from Open Food Facts.

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


class DatabaseService():

    def __init__(self):
        self.config = DB_CONFIG
        self.connect_to_db()
        self.drop_tables()
        self.create_tables()
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

    def create_tables(self):
        """
        Initializes the tables, if they do not already exist.
        """
        with open(INIT_TABLES_FILE, 'r') as f:
            with self.cnx.cursor() as cursor:
                cursor.execute(f.read(), multi=True)
        print('OK...Tables created.')

    def drop_tables(self):
        with open(CLEAR_DATA_FILE, 'r') as f:
            with self.cnx.cursor() as cursor:
                cursor.execute(f.read(), multi=True)
                self.cnx.commit()
        print('OK...Tables dropped.')
