# coding: utf-8

""" This module contains the BrandService class.
    It manages everything related to the Brands. """

import queries

import requests


class BrandService():
    
    def __init__(self, db):
        pass
        # self.get_brands(db)

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
                cursor.execute(queries.insert_brand, (brands_json['tags'][i]['name'],))
        db.cnx.commit()
        print('OK...Inserted brands into db.')