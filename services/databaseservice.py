# coding: utf-8

""" This module contains the DatabaseService class.
    It manages everything related to the database. """

import category
import queries

import requests
import mysql.connector

DB_CONFIG = {
                'user': 'purbeurre',
                'password': '123456',
                'host': '127.0.0.1',
                'database': 'purbeurre'
                }
INIT_TABLES_FILE = '/Users/julienlair/Formation_Python/projet5/app/create_tables.sql'
CLEAR_DATA_FILE = '/Users/julienlair/Formation_Python/projet5/app/drop_tables.sql'
DROP_TABLES = False


class DatabaseService():

    def __init__(self):
        self.config = DB_CONFIG
        self.connect_to_db()
        if DROP_TABLES:
            self.drop_tables()
        self.create_tables()
        self.disconnect_from_db()

    def __del__(self):
        self.disconnect_from_db()

    def connect_to_db(self):
        """
        Connects to the db, according to the config parameters given.
        config -- dict containing the configuration parameters (see constant)
        """
        self.cnx = mysql.connector.connect(**self.config)

    def disconnect_from_db(self):
        """
        Connects to the db, according to the config parameters given.
        config -- dict containing the configuration parameters (see constant)
        """
        self.cnx.close()

    def create_tables(self):
        """
        Initializes the tables, if they do not already exist.
        """
        with open(INIT_TABLES_FILE, 'r') as f:
            with self.cnx.cursor() as cursor:
                cursor.execute(f.read(), multi=True)
        print('OK...Tables created.')

    def drop_tables(self):
        with open(CLEAR_DATA_FILE, 'r') as f:
            with self.cnx.cursor() as cursor:
                cursor.execute(f.read(), multi=True)
                self.cnx.commit()
        print('OK...Tables dropped.')
