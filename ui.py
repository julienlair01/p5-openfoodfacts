# coding: utf-8
""" This module manages the user interface class. """

import os
from prettytable import PrettyTable
from prettytable import NONE
from pprint import pprint


WELCOME = '''
----------------------
       Bienvenue
----------------------

1. Trouver un substitut à un produit
2. Voir mes favoris

'''

SELECT = '''
Faîtes un choix parmi :
'''

class UI():

    def __init__(self):
        pass

    def menu_logic(self):
        pass

    def show_menu(self, categories):
        choice = ''
        while (choice not in ['1','2']):
            os.system('clear')
            print(WELCOME)
            choice = input('Quel est votre choix ? ')
        
        if choice == '1':
            return(self.choose_category(categories))
        elif choice == '2':
            self.choose_favorite()

    def choose_category(self, categories):
        print(SELECT)
        for index, value in enumerate(categories):
            print(index+1, '-', categories[index].name)
        choice = input('\nChoisissez une catégorie : ')
        return(categories[int(choice) - 1])

    def select_product(self, products):            
        os.system('clear')
        t = PrettyTable(['Choix', 'Produit'])
        t.align = 'l'
        t.vrules = NONE
        for index, value in enumerate(products):
            t.add_row([index+1, products[index].name])
        print(t)
        choice = input('\nChoisissez un produit : ')
        return(products[int(choice) - 1])

    def display_product_details(self, product):
        print('Nom : {}\nNutri-score : {}'.format(product.name, product.nutrition_score.upper()))
        os.system('clear')
        t = PrettyTable(['Détails du produit',''])
        t.align = 'l'
        t.vrules = NONE
        t.add_row(['Nom', product.name])
        t.add_row(['Nutri score', product.nutrition_score.upper()])
        t.add_row(['+ d\'infos', product.url])
        print(t)


            
    def choose_favorite(self):
        pass