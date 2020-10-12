# coding: utf-8
""" This module contains the Category class.
    It manages all interactions with one Category. """

import queries


class Category():

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_category_details(self, category_id, db):
        """
        Get Category details on Open Food Facts API.
        """
        with db.cnx.cursor(named_tuple = True) as cursor:
            cursor.execute(queries.get.category_off_id, category_id)
            print(cursor.row())
            
    def get_category_products(self):
        pass