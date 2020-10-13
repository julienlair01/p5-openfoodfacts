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
        self.brand_service = services.BrandService(self.db_service)
        self.product_service = services.ProductService()
        self.ui = ui.UI()
        
    def main_logic(self):
        self.cat_service.get_categories_from_off(self.db_service)
        self.brand_service.get_brands_from_off(self.db_service)
        categories = self.cat_service.get_categories_from_local(self.db_service)
        chosen_category = self.ui.show_menu(categories)
        products = self.product_service.get_products(self.db_service, self.cat_service, chosen_category)
        chosen_product = self.ui.select_product(products)
        self.ui.display_product_details(chosen_product)

app = App()
app.main_logic()