# coding: utf-8
""" This module contains the Product class.
    It manages all interactions with one Product. """

import queries

import mysql.connector

class Product():

    def __init__(self, db, id, name, nutrition_grade, url):
        self.id = id
        self.name = name
        self.nutrition_grade = nutrition_grade.upper()
        self.url = url
        self.brands = self.get_product_brands(db)
        self.stores = 'not available yet'

    def get_product_brands(self, db):
        """
        Get product brands.
        """
        with db.cnx.cursor(buffered=True) as cursor:
            cursor.execute(queries.get_product_brands, {'id': self.id})
            b = []
            for (name, ) in cursor:
                b.append(name)
            return ', '.join(b)

    def find_substitute(self):
        pass

