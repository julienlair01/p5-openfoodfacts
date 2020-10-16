# coding: utf-8
""" This module contains the Category class.
    It manages all interactions with one Category. """

import queries


class Category():

    def __init__(self, db, id='0', name='', off_id=''):
        self.db = db
        self.id = id
        self.name = name
        self.off_id = off_id

    def get_category_details(self, category_id):
        """
        Get Category details on Open Food Facts API.
        """
        with self.db.cnx.cursor(named_tuple = True) as cursor:
            cursor.execute(queries.get.category_off_id, category_id)
            
    def get_category_products(self):
        pass

    def insert_category_into_local(self):
        self.db.connect_to_db()
        with self.db.cnx.cursor() as cursor:
            add_category = {
                'off_id': self.off_id,
                'name': self.name
            }
            cursor.execute(queries.insert_category, add_category)
        self.db.cnx.commit()
