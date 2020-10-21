# coding: utf-8

""" This module contains the Services classes.
    It manages everything related to the Products, 
    Categories and the Database connection. """

import category
import queries
import product

from pprint import pprint
import mysql.connector
import requests

URL_PRODUCTS = 'https://fr.openfoodfacts.org/cgi/search.pl'

class ProductService():

    def __init__(self, db):
        self.products = []
        self.db = db

    def load_products(self, cat_service, category):
        """
        Checks if products already exist in the lcoal db for this category.
        If yes, returns a list of Product objects.
        If no, loads the products from Open Food Facts API.
        """
        self.db.connect_to_db()
        # faire le count
        with self.db.cnx.cursor(buffered=True) as cursor:
            cursor.execute(queries.get_products, {'cat_id': category.id})
            if cursor.rowcount > 0:
                for (id, name, nutrition_grade_fr, url, barcode) in cursor.fetchall():
                    self.products.append(product.Product(self.db, id= id, name= name, nutrition_grade= nutrition_grade_fr, url= url, barcode= barcode))
            else:
                self.load_products_from_off(cat_service, category)
                cursor.close()
                return self.load_products(cat_service, category)
        self.db.disconnect_from_db()

    def load_products_from_off(self, cat_service, category):
        """
        Retrieve the list of products of a given category, from
        the Open Food Facts API.

        db -- DatabaseService object
        cat_service -- CategoryService object
        category_id -- id of the category to get products from
        """
        print('Veuillez patienter, nous téléchargeons les produits de la catégorie {}...'.format(category.name))
        page_size = 500
        payload = {
                'action': 'process',
                'tagtype_0': 'countries',
                'tag_contains_0': 'contains',
                'tag_0': 'France',
                'tagtype_1': 'categories',
                'tag_contains_1': 'contains',
                'tag_1': category.name,
                'json': 'true',
                'page_size': page_size,
                'sort_by': 'unique_scans_n',
                'User-Agent': 'Python - find a substitute - desktop'
                }
        r = requests.get(url=URL_PRODUCTS, params=payload)
        clean_products = self.clean_products(r.json())
        for i in range(len(clean_products['products'])):
            p_buf = product.Product(
                                    db= self.db,
                                    id= 0,
                                    name= clean_products['products'][i]['product_name_fr'],
                                    nutrition_grade= clean_products['products'][i]['nutrition_grade_fr'],
                                    url= clean_products['products'][i]['url'],
                                    barcode= clean_products['products'][i]['code']
                                    )
            p_buf.insert_product_into_local(categories= clean_products['products'][i]['categories_tags'], brands= clean_products['products'][i]['brands'], stores= clean_products['products'][i]['stores'])

    def clean_products(self, products):
        """
        Method to clean products which do not have specific keys,
        contained in keys[].
        """
        keys = ['code', 'product_name_fr', 'generic_name', 'nutrition_grade_fr', 'url', 'brands', 'stores', 'categories_tags']
        for i in range(len(products['products'])):
            for j in range(len(keys)):
                try:
                    buf = products['products'][i][keys[j]]
                except KeyError:
                    products['products'][i][keys[j]] = ''
        return products