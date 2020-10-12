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

    def __init__(self, cat, db):
        self.show_menu(cat, db)

    def show_menu(self, cat, db):
        choice = ''
        while (choice not in ['1','2']):
            os.system('clear')
            print(WELCOME)
            choice = input('Quel est votre choix ? ')
        
        if choice == '1':
            self.choose_category(cat, db)
        elif choice == '2':
            self.choose_favorite()

    def choose_category(self, cat, db):
        print(SELECT_CAT)
        cat = cat.get_categories_from_local(db)
        for index, value in enumerate(cat):
            print(index, '-', cat[index].name)
        choice = ''
        choice = input('\nChoisissez une catégorie : ')
        self.chosen_category = cat[int(choice)].id

    def choose_favorite(self):
        pass