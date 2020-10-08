# coding: utf-8
""" This module contains the Database class.
    It is used by the main module for general
    interaction with the database. """

import mysql.connector
from mysql.connector import errorcode

class Database():
    """
    It manages the database connection, initialization of tables,
    and clean up of data upon user request.
    """

    def __init__(self):
        """
        This is the Database class constructor.
        """
        self.config = {
                'user': 'purbeurre',
                'password': '123456',
                'host': '127.0.0.1',
                'database': 'purbeurre',
                'raise_on_warnings': True
                }
        init_sql_file = '/Users/julienlair/Formation_Python/projet5/app/poc/db_management/create_tables.sql'
        clear_data_sql_file = '/Users/julienlair/Formation_Python/projet5/app/database.py'

    def connect_to_db(self):
        """
        Connects to the db, using the config specified
        in the constructor.
        """
        self.cnx = mysql.connector.connect(**config)
        self.cnx.raise_on_warnings = False
    
    def disconnect_from_db(self):
        """
        Disconnects from db.
        """
        self.cnx.close()

    def init_tables(self, init_sql_file):
        cursor = self.cnx.cursor()
        cursor.execute(init_sql_file)
        self.cnx.commit()
        cursor.close()

    def clear_data(self, clear_data_sql_file):
        cursor = self.cnx.cursor()
        cursor.execute(clear_data_sql_file)
        self.cnx.commit()
        cursor.close()