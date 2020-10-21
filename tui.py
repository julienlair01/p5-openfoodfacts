# coding: utf-8
""" This module manages the terminal user interface class. """

import os
from prettytable import PrettyTable
from prettytable import NONE, ALL, PLAIN_COLUMNS
from pprint import pprint


class TUI():

    def __init__(self):
        self.menu_choices = ['Trouver un substitut sain à un produit', 'Voir les produits sauvegardés', 'Quitter']
        self.table_style = {'align': 'l', 'vrules': NONE}

    def menu_logic(self):
        pass

    def show_menu(self, categories):
        choice = ''
        os.system('clear')
        while choice not in [1,2]:
            t = PrettyTable(['Choix', ''], **self.table_style)
            for index, value in enumerate(self.menu_choices):
                t.add_row([index+1, value])
            print(t)
            choice = input('\nQue shouhaitez-vous faire ? ')

            if choice == '1':
                return(self.select_category(categories))
            elif choice == '2':
                self.choose_favorite()
            else:
                print('\nVeuillez entrer un choix valide.\n')

    def select_category(self, categories):
        os.system('clear')
        t = PrettyTable(['Choix', 'Categorie'], **self.table_style)
        for index, value in enumerate(categories):
            t.add_row([index+1, categories[index].name])
        print(t)
        choice = input('\nChoisissez une catégorie : ')
        return(categories[int(choice) - 1])

    def select_product(self, products):
        choice = 'S'
        min = 0
        while choice in ('P', 'S'):
            os.system('clear')
            t = PrettyTable(['Choix', 'Produit', 'Marques', 'Nutri-score'], **self.table_style)
            
            if min >= 20:
                t.add_row(['P', 'Page précédente','',''])
                t.add_row(['', '','',''])
            try:
                for index in range(min, min+20):
                    t.add_row([index+1, products[index].name, products[index].brands, products[index].nutrition_grade.upper()])
            except IndexError:
                pass
            if (min + 20) < len(products):
                t.add_row(['', '','',''])
                t.add_row(['S', 'Page suivante','',''])
            print(t)
            choice = input('\nChoisissez un produit : ').upper()
            if choice == 'S':
                min += 20
            elif choice == 'P':
                min -= 20
        return(products[int(choice) - 1])

    def display_product_details(self, product):
        os.system('clear')
        t = PrettyTable(['Détails du produit sélectionné',''], **self.table_style)
        t.add_row(['Marques', product.brands])
        t.add_row(['Nom', product.name])
        t.add_row(['Nutri score', product.nutrition_grade])
        t.add_row(['Distributeurs', product.stores])
        t.add_row(['+ d\'infos', product.url])
        print(t)

    def choose_favorite(self):
        pass