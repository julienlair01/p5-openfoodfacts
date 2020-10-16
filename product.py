# coding: utf-8
""" This module contains the Product class.
    It manages all interactions with one Product. """

import queries

import mysql.connector

class Product():

    def __init__(self, db, id, name, nutrition_grade, url, barcode):
        self.db = db
        self.id = id
        self.name = name
        self.nutrition_grade = nutrition_grade.upper()
        self.url = url
        self.barcode = barcode
        self.brands = self.get_product_brands()
        self.stores = 'not available yet'

    def get_product_brands(self):
        """
        Get product brands. Returns a string, 
        concatenating all product brands.

        db -- DatabaseService object
        """
        with self.db.cnx.cursor(buffered=True) as cursor:
            cursor.execute(queries.get_product_brands, {'id': self.id})
            b = []
            for (name, ) in cursor:
                b.append(name)
            return ', '.join(b)

    def insert_product_into_local(self, category, brands, stores):
        """
        Insert a product into the local database.
        Stores the relationship between product and category
        in the local database.
        Stores the relationship between product and brands in
        the local database

        category -- Category object
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
            self.save_product_category(cursor, category, last_product_id)
            self.save_product_brand(cursor, brands, last_product_id)
            self.save_product_store(cursor, stores, last_product_id)
        self.db.cnx.commit()

    def save_product_category(self, cursor, category, last_product_id):
        add_product_category = {
                'product_id': last_product_id,
                'category': category.off_id,
            }
        cursor.execute(queries.insert_product_category, add_product_category)

    def save_product_brand(self, cursor, brands, last_product_id):
        buf_brands = brands.split(',') 
        for j in range(len(buf_brands)):
            add_product_brand = {
                'product_id': last_product_id,
                'brand': buf_brands[j]
            }
            cursor.execute(queries.insert_product_brand, add_product_brand)

    def save_product_store(self, cursor, stores, last_product_id):
        buf_stores = stores.split(',') 
        print('Store :', stores, buf_stores)
        for j in range(len(buf_stores)):
            add_product_store = {
                'product_id': last_product_id,
                'store': buf_stores[j]
            }
            cursor.execute(queries.insert_product_store, add_product_store)

    def find_substitute(self):
        pass

