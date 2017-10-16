#! /usr/bin/env python3
# #-*- coding: utf-8 -*-

from math import ceil
import database as db


############################
# Page classes and methods #
############################
""" Module that manages pages of data for user experience
"""

class PageCategories():
    """ Class that creates pages for the selection Menu
    Each page has its own methods to fetch data from
    the database
    """
    CAT_PAGES_INDEX = []
    OFFSET = 10

    def __init__(self, index):
        """ Class initializer
        """
        connection = db.connect()
        self.entries_list = db.req_categories_for_page_entries(connection, \
                                                               index*self.OFFSET, \
                                                               self.OFFSET)
        db.disconnect(connection)

    @classmethod
    def get_number_cat(cls):
        """ Class method that retrieves the number of categories
        """
        connection = db.connect()
        nb_cat = db.req_categories_count(connection)
        db.disconnect(connection)
        return nb_cat

    @classmethod
    def initiates_index(cls):
        """ Class method that creates the index of pages
        """
        nb_cat = cls.get_number_cat()
        nb_pages_cat = int(ceil(nb_cat / cls.OFFSET))
        for page_number in range(nb_pages_cat):
            page = PageCategories(page_number)
            cls.CAT_PAGES_INDEX.append(page)


class PageProducts(PageCategories):
    """ Subclass with its own methods for products
    retrieval, with its own requests methods
    """
    PROD_PER_CAT_PAGES_INDEX = []

    def __init__(self, index, name_category_fr):
        """ Class initializer
        """
        connection = db.connect()
        self.entries_list = db.req_products_for_page_entries(connection, \
                                                             name_category_fr, \
                                                             index*self.OFFSET, \
                                                             self.OFFSET)
        db.disconnect(connection)

    @classmethod
    def initiates_prod_index(cls, name_category_fr):
        """Class method that creates the index of pages
        """
        connection = db.connect()
        nb_prod_per_cat = db.req_products_per_cat_count(connection, \
                                                        name_category_fr)
        nb_pages_prod_per_cat = int(ceil(nb_prod_per_cat / cls.OFFSET))
        for page_number in range(nb_pages_prod_per_cat):
            page_prod = PageProducts(page_number, name_category_fr)
            cls.PROD_PER_CAT_PAGES_INDEX.append(page_prod)
        db.disconnect(connection)


class PageRecommandation(PageCategories):
    """ Subclass with its own methods for recommandations
    retrieval, with its own requests methods
    """
    def __init__(self, name_category_fr, ps_name, ps_brand, ps_quantity):
        """ Class initializer
        """
        connection = db.connect()
        self.entries_list = db.req_recommandations(connection, \
                                                   name_category_fr, \
                                                   ps_name, \
                                                   ps_brand, \
                                                   ps_quantity, \
                                                   self.OFFSET)
        db.disconnect(connection)


class PageSaves(PageCategories):
    """ Subclass with its own methods for saved recommandations
    retrieval, with its own requests methods
    """
    SAVES_PAGES_INDEX = []
    def __init__(self, index):
        """ Class initializer
        """
        connection = db.connect()
        self.entries_list = db.req_saves(connection, \
                                         index*self.OFFSET, \
                                         self.OFFSET)
        db.disconnect(connection)

    @classmethod
    def initiates_saves_index(cls):
        """Class method that creates the index of pages
        """
        connection = db.connect()
        nb_saves = db.req_saves_count(connection)
        nb_pages_saves = int(ceil(nb_saves / cls.OFFSET))
        for page_number in range(nb_pages_saves):
            page_save = PageSaves(page_number)
            cls.SAVES_PAGES_INDEX.append(page_save)
        db.disconnect(connection)
