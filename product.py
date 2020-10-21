# coding: utf-8
""" This module contains the Product class.
    It manages all interactions with one Product. """

import queries

import mysql.connector
from pprint import pprint

class Product():

    def __init__(self, db, id, name, nutrition_grade, url, barcode):
        self.db = db
        self.id = id
        self.name = name
        self.nutrition_grade = nutrition_grade.upper()
        self.url = url
        self.barcode = barcode
        self.categories = self.get_product_categories()
        self.brands = self.get_product_brands()
        self.stores = self.get_product_stores()

    def get_product_categories(self):
        """
        Get product categories. Returns a string, 
        concatenating all product categories.
        """
        with self.db.cnx.cursor(buffered=True) as cursor:
            cursor.execute(queries.get_product_categories, {'id': self.id})
            c = []
            for (name, ) in cursor:
                c.append(name)
            return ', '.join(c)

    def get_product_brands(self):
        """
        Get product brands. Returns a string, 
        concatenating all product brands.
        """
        with self.db.cnx.cursor(buffered=True) as cursor:
            cursor.execute(queries.get_product_brands, {'id': self.id})
            b = []
            for (name, ) in cursor:
                b.append(name)
            return ', '.join(b)

    def get_product_stores(self):
        """
        Get product stores. Returns a string, 
        concatenating all product stores.
        """
        with self.db.cnx.cursor(buffered=True) as cursor:
            cursor.execute(queries.get_product_stores, {'id': self.id})
            s = []
            for (name, ) in cursor:
                s.append(name)
            return ', '.join(s)

    def insert_product_into_local(self, categories, brands, stores):
        """
        Insert a product into the local database.
        Stores the relationship between product and category
        in the local database.
        Stores the relationship between product and brands in
        the local database

        categories -- Category object
        brands -- str with all product brands
        """
        add_product = {
            'barcode': self.barcode,
            'name_fr': self.name,
            'nutrition_grade_fr': self.nutrition_grade,
            'url': self.url
        }
        with self.db.cnx.cursor() as cursor:
            cursor.execute(queries.insert_product, add_product)  
            last_product_id = cursor.lastrowid
            self.save_product_category(cursor, categories, last_product_id)
            self.save_product_brand(cursor, brands, last_product_id)
            self.save_product_store(cursor, stores, last_product_id)
        self.db.cnx.commit()

    def save_product_category(self, cursor, categories_tags, last_product_id):
        buf_categories = []
        [buf_categories.append(value) for value in categories_tags]
        for i in range(len(buf_categories)):
            add_product_category = {
                    'product_id': last_product_id,
                    'category': buf_categories[i]
                }
            cursor.execute(queries.insert_product_category, add_product_category)

    def save_product_brand(self, cursor, brands, last_product_id):
        buf_brands = brands.split(',') 
        for j in range(len(buf_brands)):
            add_product_brand = {
                'product_id': last_product_id,
                'brand': buf_brands[j]
            }
            cursor.execute(queries.insert_brand, (buf_brands[j],))
            cursor.execute(queries.insert_product_brand, add_product_brand)

    def save_product_store(self, cursor, stores, last_product_id):
        buf_stores = stores.split(',') 
        for j in range(len(buf_stores)):
            add_product_store = {
                'product_id': last_product_id,
                'store': buf_stores[j]
            }
            cursor.execute(queries.insert_store, (buf_stores[j],))
            cursor.execute(queries.insert_product_store, add_product_store)
    
    def save_product_substitute(self, substitute_id, score):
        with self.db.cnx.cursor(buffered=True) as cursor:
            cursor.execute(queries.insert_product_substitute, {'product_id': self.id, 'substitute_id': substitute_id, 'score': score})
            self.db.cnx.commit()

    def find_substitute(self):
        """
        Method to find a substitute to the given product.
        Finds all products with one category in common and 
        best possible nutrition grade.
        """
        substitutes=[]
        test_list1 = []

        self.db.connect_to_db()
        with self.db.cnx.cursor(buffered=True, dictionary=True) as cursor:
            cursor.execute(queries.find_substitute, {'id': self.id})
            if cursor.rowcount == 0:
                print("no substitute found")
            else:
                for id in cursor:
                    test_list2 = []
                    with self.db.cnx.cursor(buffered=True, dictionary=True) as cursor:
                        cursor.execute(queries.get_product_categories, {'id': id['id']})
                        [test_list2.append(result['category name']) for result in cursor]
                    score = len(set(self.categories) & set(','.join(test_list2))) / float(len(set(self.categories) | set(','.join(test_list2)))) * 100
                    if score >= 50:
                        self.save_product_substitute(id['id'], score)
        self.db.disconnect_from_db()

