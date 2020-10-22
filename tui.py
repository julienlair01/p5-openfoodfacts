# coding: utf-8
""" This module manages the terminal user interface class. """

import os
from prettytable import PrettyTable
from prettytable import NONE, ALL, PLAIN_COLUMNS
from pprint import pprint


class TUI():

    def __init__(self):
        self.menu_choices = ['Trouver un substitut sain à un produit', 'Voir les produits sauvegardés', 'Quitter']
        self.save_choices = ['Sauvegarder ce produit de substituion', 'Chercher un nouveau produit', 'Quitter']
        self.table_style = {'align': 'l', 'vrules': NONE}

    def menu_logic(self):
        pass

    def show_menu(self):
        choice = ''
        os.system('clear')
        t = PrettyTable(['Choix', ''], **self.table_style)
        for index, value in enumerate(self.menu_choices):
            t.add_row([index+1, value])
        print(t)
        choice = input('\nQue souhaitez-vous faire ? ')
        if choice in ['1', '2']:
            return choice
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
        t.add_row(['Id', product.id])
        t.add_row(['Marques', product.brands])
        t.add_row(['Nom', product.name])
        t.add_row(['Nutri score', product.nutrition_grade])
        t.add_row(['Distributeurs', product.stores])
        t.add_row(['+ d\'infos', product.url])
        print(t)

    def display_product_substitute(self, substitute):
        print('\n')
        t = PrettyTable(['Voici un produit plus sain !   ',''], **self.table_style)
        t.add_row(['Id', substitute.id])
        t.add_row(['Marques', substitute.brands])
        t.add_row(['Nom', substitute.name])
        t.add_row(['Nutri score', substitute.nutrition_grade])
        t.add_row(['Distributeurs', substitute.stores])
        t.add_row(['+ d\'infos', substitute.url])
        print(t)
    
    def save_favorite(self):
        t = PrettyTable(['\nChoix', ''], vrules= NONE, hrules= NONE, align= 'l')
        for index, value in enumerate(self.save_choices):
            t.add_row([index+1, value])
        print(t)
        return input('\nQue souhaitez-vous faire ? ')

    def display_favorites(self):
        pass