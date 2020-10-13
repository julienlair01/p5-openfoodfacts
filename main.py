# coding: utf-8
""" 

"""

from services import services
import ui

from pprint import pprint


class App():
    def __init__(self):
        self.db_service = services.DatabaseService()
        self.cat_service = services.CategoryService(self.db_service)
        self.product_service = services.ProductService()
        self.ui = ui.UI()
        
    def main_logic(self):
        self.cat_service.get_categories_from_off(self.db_service)
        categories = self.cat_service.get_categories_from_local(self.db_service)
        chosen_category = self.ui.show_menu(categories)
        self.products = self.product_service.get_products(self.db_service, self.cat_service, chosen_category)
        print(self.products)

app = App()
app.main_logic()

# product_service = services.ProductService()
# product_service.get_products_from_off(id, db_service, cat_service)
