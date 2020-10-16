# coding: utf-8

""" This module contains the CategoryService class.
    It manages everything related to the Categories. """

import category
import queries

import requests


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