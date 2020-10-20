# coding: utf-8

""" This module contains the CategoryService class.
    It manages everything related to the Categories. """

import category
import queries

import requests

FILTER_CATEGORIES = [
            'Fromages',
            'Boissons',
            'Plats préparés',
            'Produits laitiers'
        ]

class CategoryService():
    
    def __init__(self, db):
        self.categories = []
        self.main_categories = []
        self.db = db
        self.load_categories()
        self.get_main_categories()

    def load_categories(self):
        """
        Load categories, from local db if they exist,
        or from Open Food Facts if they do not.
        List Caterogy object in categories[]
        
        db -- DatabaseService object
        """
        self.load_categories_from_local()
        if self.categories == []:
            self.load_categories_from_off()
            self.load_categories_from_local()
        else:
            print('OK...Categories already exist locally.') 

    def load_categories_from_off(self):
        """  
        Get all categories from Open Food Facts and keeps only
        the ones speciafied in filter_categories.

        db -- Database object
        """
        cat_json  = requests.get('https://fr.openfoodfacts.org/categories.json').json()
        print('OK...Categories retrieved from Open Food Facts.') 
        for i in range(len(cat_json['tags'])):
            c_buf = category.Category(
                db = self.db,
                name = cat_json['tags'][i]['name'],
                off_id = cat_json['tags'][i]['id']
            )
            c_buf.insert_category_into_local()
        print('OK...Inserted categories into db.')

    def load_categories_from_local(self):
        """
        Get categories from local db.
        Returns a list of Category objects.

        db -- Database object
        """
        self.db.connect_to_db()
        with self.db.cnx.cursor(named_tuple = True, buffered = True) as cursor:
            cursor.execute(queries.get_categories)
            if cursor.rowcount > 0:
                for (id, name, off_id) in cursor:
                    self.categories.append(category.Category(db= self.db, id= id, name= name, off_id= off_id))
        self.db.disconnect_from_db()

    def get_main_categories(self):
        for category in self.categories:
            if category.name in FILTER_CATEGORIES:
                self.main_categories.append(category)
