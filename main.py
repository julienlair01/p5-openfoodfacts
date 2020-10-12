# coding: utf-8
""" 

"""

import services

from pprint import pprint

db_service = services.DatabaseService()
services.CategoryService(db_service)
product_service = services.ProductService()
# product_service.get_products_from_off('fr:pates-a-tartiner', db_service)
