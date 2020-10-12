# coding: utf-8
""" 

"""

from services import services
import ui

from pprint import pprint

db_service = services.DatabaseService()
cat_service = services.CategoryService(db_service)
product_service = services.ProductService()
ui = ui.UI(cat_service, db_service)
product_service.get_products_from_off(id, db_service, cat_service)
