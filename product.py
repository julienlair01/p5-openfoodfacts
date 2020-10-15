# coding: utf-8
""" This module contains the Product class.
    It manages all interactions with one Product. """


class Product():

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.nutrition_grade = 'not available yet'
        self.url = 'not available yet'
        self.brands = 'not available yet'
        self.stores = 'not available yet'

    def get_product_details(self):
        """
        Get product details on Open Food Facts API.
        """
        pass

    def find_substitute(self):
        pass

