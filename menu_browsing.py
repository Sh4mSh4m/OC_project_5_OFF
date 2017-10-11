#! /usr/bin/env python3
# #-*- coding: utf-8 -*-


import pymysql.cursors
import database as db
from math import ceil

class Page_categories():
    """ Class that creates pages for the selection Menu
    Each page has its own methods to fetch data from 
    the database and will display data for the user 
    to make his selection
    """
    CAT_PAGES_INDEX = []
    OFFSET = 10

    def __init__(self, index):
        connection = db.connect()
        self.entries_list = db.req_categories_for_page_entries(connection, index*self.OFFSET, self.OFFSET)
        db.disconnect(connection)

    # Merge with the other class method
    @classmethod
    def calculates_pages(cls):
        """Class method that retrives the number of categories"""
        connection = db.connect()
        nb_cat = db.req_categories_count(connection)
        db.disconnect(connection)
        return nb_cat

    @classmethod
    def initiates_index(cls):
        """Class method that creates the index of pages"""
        nb_cat = cls.calculates_pages()
        nb_pages_cat = int(ceil(nb_cat / cls.OFFSET))
        for page_number in range(nb_pages_cat):
            page = Page_categories(page_number)
            cls.CAT_PAGES_INDEX.append(page)

    def displays_categories(self):
        """ Method that displays the content of a page
        """
        print("\nBelow, categories to choose from:\n")
        # Using len(), because last page may have less items
        for i in range(len(self.entries_list)):
            print("{} - {}".format(i + 1, self.entries_list[i]['name_category_fr']))
        print("\nPlease, select category with corresponding number:")


class Page_products(Page_categories):
    """ Subclass with its own methods for products
    retrieval, with its own requests methods
    """
    PROD_PER_CAT_PAGES_INDEX = []

    def __init__(self, index, name_category_fr):
        connection = db.connect()
        self.entries_list = db.req_products_for_page_entries(connection, name_category_fr, index*self.OFFSET, self.OFFSET)
        db.disconnect(connection)

    @classmethod
    def initiates_prod_index(cls, name_category_fr):
        """Class method that creates the index of pages"""
        connection = db.connect()
        nb_prod_per_cat = db.req_products_per_cat_count(connection, name_category_fr)
        # draft
        nb_pages_prod_per_cat = int(ceil(nb_prod_per_cat / cls.OFFSET))
        for page_number in range(nb_pages_prod_per_cat):
            page_prod = Page_products(page_number, name_category_fr)
            cls.PROD_PER_CAT_PAGES_INDEX.append(page_prod)
        db.disconnect(connection)

    def displays_products(self):
        """ Method that displays the content of a page
        """
        print("\nBelow, categories to choose from:\n")
        # Using len(), because last page may have less items
        for i in range(len(self.entries_list)):
            print("{} - {}".format(i + 1, self.entries_list[i]['name_product']))
        print("\nPlease, select product with corresponding number:")

class Page_recommandation(Page_categories):

    def __init__(self,name_category_fr, product_selected):
        connection = db.connect()
        self.entries_list = db.req_recommandations(connection, name_category_fr, product_selected, self.OFFSET)
        db.disconnect(connection)

    def displays_recommandations(self):
        """ Method that displays the content of a page
        """
        print("\nBelow, categories to choose from:\n")
        # Using len(), because last page may have less items
        for i in range(len(self.entries_list)):
            print("{} - {} {} {}".format(i + 1, \
                self.entries_list[i]['name_product'], \
                self.entries_list[i]['brand'], \
                self.entries_list[i]['quantity']))
        print("\nPlease, select recommandation with corresponding number:")


class Page_saves(Page_categories):

    SAVES_PAGES_INDEX = []
    def __init__(self, index):
        connection = db.connect()
        self.entries_list = db.req_saves(connection, index*self.OFFSET, self.OFFSET)
        db.disconnect(connection)

    @classmethod
    def initiates_saves_index(cls):
        """Class method that creates the index of pages"""
        connection = db.connect()
        nb_saves = db.req_saves_count(connection)
        nb_pages_saves = int(ceil(nb_saves / cls.OFFSET))
        for page_number in range(nb_pages_saves):
            page_save = Page_saves(page_number)
            cls.SAVES_PAGES_INDEX.append(page_save)
        db.disconnect(connection)

    def displays_saves(self):
        """ Method that displays the content of a page
        """
        print("\nBelow, saves to choose from:\n")
        # Using len(), because last page may have less items
        for i in range(len(self.entries_list)):
            print("{} - {} {} {}".format(i + 1, \
                self.entries_list[i]['name_product'], \
                self.entries_list[i]['brand'], \
                self.entries_list[i]['quantity']))
        print("\nPlease, select recommandation with corresponding number:")