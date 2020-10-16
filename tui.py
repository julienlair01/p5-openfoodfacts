# coding: utf-8
""" This module manages the terminal user interface class. """

import os
from prettytable import PrettyTable
from prettytable import NONE
from pprint import pprint


class TUI():

    def __init__(self):
        pass

    def menu_logic(self):
        pass

    def show_menu(self, categories):
        choice = ''
        os.system('clear')
        while choice not in [1,2]:
            print('''Bienvenue !
1 - Trouver un subsitut plus sain à produit
2 - Voir la liste de mes favoris\n'''
                )       
            choice = input('Quel est votre choix ? ')
            if choice == '1':
                return(self.select_category(categories))
            elif choice == '2':
                self.choose_favorite()
            else:
                print('\nVeuillez entrer un choix valide.\n')

    def select_category(self, categories):
        os.system('clear')
        t = PrettyTable(['Choix', 'Categorie'])
        t.align = 'l'
        t.vrules = NONE
        for index, value in enumerate(categories):
            t.add_row([index+1, categories[index].name])
        print(t)
        choice = input('\nChoisissez une catégorie : ')
        return(categories[int(choice) - 1])

    def select_product(self, products):
        os.system('clear')
        t = PrettyTable(['Choix', 'Produit', 'Marques'])
        t.align = 'l'
        t.vrules = NONE
        for index, value in enumerate(products):
            t.add_row([index+1, products[index].name, products[index].brands])
        print(t)
        choice = input('\nChoisissez un produit : ')
        return(products[int(choice) - 1])

    def display_product_details(self, product):
        os.system('clear')
        t = PrettyTable(['Détails du produit',''])
        t.align = 'l'
        t.vrules = NONE
        t.add_row(['Marques', product.brands])
        t.add_row(['Nom', product.name])
        t.add_row(['Nutri score', product.nutrition_grade])
        t.add_row(['Distributeurs', product.stores])
        t.add_row(['+ d\'infos', product.url])
        print(t)

    def choose_favorite(self):
        pass