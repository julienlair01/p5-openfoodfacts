# coding: utf-8
""" 

"""

from services import productservice, categoryservice, databaseservice, brandservice
import tui
import product

from pprint import pprint


class App():

    def __init__(self):
        self.db_service = databaseservice.DatabaseService()
        self.cat_service = categoryservice.CategoryService(self.db_service)
        self.brand_service = brandservice.BrandService(self.db_service)
        self.product_service = productservice.ProductService(self.db_service)
        self.tui = tui.TUI()
        
    def main_logic(self):
        chosen_category = self.tui.show_menu(self.cat_service.main_categories)
        self.product_service.load_products(self.cat_service, chosen_category)
        chosen_product = self.tui.select_product(self.product_service.products)
        chosen_product.find_substitute()
        self.tui.display_product_details(chosen_product)

app = App()
app.main_logic()