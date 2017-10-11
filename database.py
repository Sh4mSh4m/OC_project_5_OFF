#! /usr/bin/env python3
# #-*- coding: utf-8 -*-

import pymysql.cursors

def connect():
    # Connect to the database with credentials
    # login and pwd to be removed and put in config file
    connection = pymysql.connect(host='localhost',
                                 user='sql_script',
                                 password='hieuhieu81',
                                 db='off',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)#
    return connection

def disconnect(connection):
    # Closes the connection to the DB
    connection.close()

def req_categories_count(connection):
    # returns total number of categories
    with connection.cursor() as cursor:
        # Read a single record
        sql = """SELECT COUNT(*)
               FROM Categories"""
        cursor.execute(sql)
        # We retrieve a single value from the dict
        result = cursor.fetchone()['COUNT(*)']
        return result

def req_products_per_cat_count(connection, name_category_fr):
    # returns total number of categories
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
        # We retrieve a single value from the dict
        result = cursor.fetchone()['COUNT(*)']
        return result

def req_saves_count(connection):
    # returns total number of categories
    with connection.cursor() as cursor:
        # Read a single record
        sql = """SELECT COUNT(*)
               FROM Saves"""
        cursor.execute(sql)
        # We retrieve a single value from the dict
        result = cursor.fetchone()['COUNT(*)']
        return result

def req_categories_for_page_entries(connection, index, length):
    with connection.cursor() as cursor:
        # Read a sample of categories
        sql = """SELECT name_category_fr 
               FROM Categories LIMIT %s, %s"""
        cursor.execute(sql, (index, length))
        # We retrieve a list of dict
        result = cursor.fetchall()
        return result

def req_products_for_page_entries(connection, name_category_fr, index, length):
    with connection.cursor() as cursor:
        # Read a sample of products
        sql = """SELECT PC.name_category_fr_b, P.name_product, P.brand, P.quantity, P.nutrition
              FROM Product_category as PC 
              INNER JOIN Products as P 
              ON PC.name_product_b = P.name_product 
              WHERE (PC.name_category_fr_b = %s) 
              AND (P.name_product <> ' ') 
              LIMIT %s,%s"""
        cursor.execute(sql, (name_category_fr, index, length))
        result = cursor.fetchall()
        return result

def req_recommandations(connection, name_category_fr, product_selected, length):
    with connection.cursor() as cursor:
        # Read a sample of products
        sql = """SELECT P.id, P.name_product, P.brand, P.quantity
              FROM Product_category as PC 
              INNER JOIN Products as P 
              ON PC.name_product_b = P.name_product 
              WHERE (PC.name_category_fr_b = %s) 
              AND (P.name_product <> ' ') 
              AND (P.nutrition IS NOT NULL)
              AND (P.name_product NOT LIKE %s )
              ORDER BY P.nutrition
              LIMIT %s"""
        cursor.execute(sql, (name_category_fr, product_selected + '%', length))
        result = cursor.fetchall()
        return result

def req_saves(connection, index, length):
    with connection.cursor() as cursor:
        # Read a sample of saves
        sql = """SELECT * 
               FROM Saves as S
               INNER JOIN Products as P
               WHERE S.saved_product_id = P.id
               LIMIT %s, %s"""
        cursor.execute(sql, (index, length))
        # We retrieve a list of dict
        result = cursor.fetchall()
        return result

def push_saves(recommandation_dict):
    connection = connect()
    with connection.cursor() as cursor:
        # Create a new record
        sql = """INSERT IGNORE INTO Saves
               (saved_product_id)
               VALUES (%s)"""
        cursor.execute(sql, (recommandation_dict['Product.id'],))
    connection.commit()
    connection.close()
