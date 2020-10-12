# coding: utf-8
""" This module contains the Category class.
    It manages all interactions with one Category. """


class Category():

    def __init__(self, off_id, name):
        self.off_id = off_id
        self.name = name

    def get_category_details(self):
        """
        Get Category details on Open Food Facts API.
        """
        pass

    def get_category_products(self):
        pass