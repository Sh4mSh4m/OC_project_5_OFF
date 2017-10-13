#! /usr/bin/env python3
# #-*- coding: utf-8 -*-

import json
import pymysql.cursors

##########################
# SQL requests functions #
##########################
""" Module that manages functions to send requests to the database
"""

def connect():
    """ Connect to the database with credentials
    """
    db_cred = json.load(open("db_cred.json"))
    connection = pymysql.connect(host='localhost',
                                 user=db_cred['user'],
                                 password=db_cred['password'],
                                 db='off',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def disconnect(connection):
    """ Closes the connection to the DB
    """
    connection.close()

def req_categories_count(connection):
    """ returns total number of categories
    """
    with connection.cursor() as cursor:
        # Read a single record
        sql = """SELECT COUNT(*)
               FROM Categories"""
        cursor.execute(sql)
        # Retrieves a dict
        result = cursor.fetchone()['COUNT(*)']
        return result

def req_products_per_cat_count(connection, name_category_fr):
    """ returns total number of categories
    """
    with connection.cursor() as cursor:
        # Read a single record
        sql = """SELECT COUNT(*)
              FROM Product_category as PC 
              INNER JOIN Products as P 
              ON PC.name_product_b = P.name_product 
              WHERE (PC.name_category_fr_b = %s) 
              AND (P.name_product <> ' ')
              ORDER BY name_product"""
        cursor.execute(sql, (name_category_fr,))
        # Retrieves a dict
        result = cursor.fetchone()['COUNT(*)']
        return result

def req_saves_count(connection):
    """ returns total number of categories
    """
    with connection.cursor() as cursor:
        # Read a single record
        sql = """SELECT COUNT(*)
               FROM Saves"""
        cursor.execute(sql)
        # Retrieves a dict
        result = cursor.fetchone()['COUNT(*)']
        return result

def req_categories_for_page_entries(connection, \
                                    index, \
                                    length):
    """ Returns a selection of categories
    """
    with connection.cursor() as cursor:
        sql = """SELECT name_category_fr
               FROM Categories LIMIT %s, %s"""
        cursor.execute(sql, (index, length))
        # Retrieves a list of dict
        result = cursor.fetchall()
        return result

def req_products_for_page_entries(connection, \
                                  name_category_fr, \
                                  index, \
                                  length):
    """ Returns a selection of products
    """
    with connection.cursor() as cursor:
        sql = """SELECT PC.name_category_fr_b,
                        P.name_product, 
                        P.brand, 
                        P.quantity, 
                        P.nutrition
              FROM Product_category as PC 
              INNER JOIN Products as P 
              ON PC.name_product_b = P.name_product 
              WHERE (PC.name_category_fr_b = %s) 
              AND (P.name_product <> ' ') 
              LIMIT %s,%s"""
        cursor.execute(sql, (name_category_fr, index, length))
        # Retrieves a list of dict
        result = cursor.fetchall()
        return result

def req_recommandations(connection, \
                        name_category_fr, \
                        ps_name, \
                        ps_brand, \
                        ps_quantity, \
                        length):
    """ Returns a selection of recommandations
    """
    with connection.cursor() as cursor:
        sql = """SELECT P.id,
                        P.name_product, 
                        P.brand, 
                        P.quantity, 
                        P.nutrition, 
                        P.description, 
                        P.url
              FROM Product_category as PC 
              INNER JOIN Products as P 
              ON PC.name_product_b = P.name_product 
              WHERE (PC.name_category_fr_b = %s) 
              AND (P.name_product <> ' ') 
              AND (P.nutrition IS NOT NULL)
              AND (P.name_product NOT LIKE %s )
              AND (P.brand NOT LIKE %s )
              AND (P.quantity NOT LIKE %s )
              ORDER BY P.nutrition
              LIMIT %s"""
        cursor.execute(sql, (name_category_fr, \
                             ps_name + '%', \
                             ps_brand + '%', \
                             ps_quantity + '%', \
                             length))
        # Retrieves a list of dict
        result = cursor.fetchall()
        return result

def req_saves(connection, index, length):
    """ Returns a selection of saved recommandations
    """
    with connection.cursor() as cursor:
        # Read a sample of saves
        sql = """SELECT *
               FROM Saves as S
               INNER JOIN Products as P
               WHERE S.saved_product_id = P.id
               LIMIT %s, %s"""
        cursor.execute(sql, (index, length))
        # Retrieves a list of dict
        result = cursor.fetchall()
        return result

def push_saves(recommandation_dict):
    """ Writes recommandation in the database
    """
    connection = connect()
    with connection.cursor() as cursor:
        # Create a new record
        sql = """INSERT IGNORE INTO Saves
               (saved_product_id)
               VALUES (%s)"""
        cursor.execute(sql, (recommandation_dict['id'],))
    connection.commit()
    connection.close()
