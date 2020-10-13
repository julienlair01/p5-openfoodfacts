# coding: utf-8
""" This module manages the user interface class. """

import os

from pprint import pprint

WELCOME = '''
----------------------
       Bienvenue
----------------------

1. Trouver un substitut à un produit
2. Voir mes favoris

'''

SELECT_CAT = '''
Choisissez la catégorie du produit à substituer :
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
        print(SELECT_CAT)
        for index, value in enumerate(categories):
            print(index+1, '-', categories[index].name)
        choice = input('\nChoisissez une catégorie : ')
        return(categories[int(choice) - 1])

    def choose_favorite(self):
        pass