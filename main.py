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
        choice_main_menu = ''
        while choice_main_menu not in ['1','2']:
            choice_main_menu = self.tui.show_menu()
            if choice_main_menu == '1':
                chosen_category = self.tui.select_category(self.cat_service.main_categories)
                self.product_service.load_products(self.cat_service, chosen_category)
                chosen_product = self.tui.select_product(self.product_service.products)
                chosen_product.find_substitutes()
                self.tui.display_product_details(chosen_product)
                self.tui.display_product_substitute(chosen_product.get_substitute())
                if self.tui.save_favorite() == '1':
                    chosen_product.save_favorite()
            elif choice_main_menu == '2':
                pass
            elif choice_main_menu == '3':
                pass

    
app = App()
app.main_logic()