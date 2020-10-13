# coding: utf-8
""" This module contains the Product class.
    It manages all interactions with one Product. """


class Product():

    def __init__(self, barcode, name, nutrition_score, url):
        self.barcode = barcode
        self.name = name
        self.nutrition_score = nutrition_score
        self.url = url

    def get_product_details(self):
        """
        Get product details on Open Food Facts API.
        """
        pass

    def find_substitute(self):
        pass

