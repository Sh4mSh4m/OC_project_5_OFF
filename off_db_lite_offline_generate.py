"""
OpenFoodFacts OPENCLASSROOMS PROJECT 5 by hieu2d@gmail.com
"""
#! /usr/bin/env python3
# #-*- coding: utf-8 -*-

import requests
import pymysql.cursors
import math
import datetime
import json

#######################
# Database initiation #
#######################

def db_connect():
    """ Connects to the database
    """
    db_cred = json.load(open("db_cred.json"))
    connection = pymysql.connect(host='localhost',
                                 user=db_cred['user'],
                                 password=db_cred['password'],
                                 db='off',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def db_init():
    """ Function that initiates the tables and sets the keys and indexes
    """
    sql_dtable_categories = "DROP TABLE IF EXISTS Categories"
    sql_ctable_categories = "CREATE TABLE Categories (\
                                 id INT UNSIGNED AUTO_INCREMENT,\
                                 name_category_fr VARCHAR(200) NOT NULL,\
                                 name_category VARCHAR(200) NOT NULL,\
                                 nb_products INT UNSIGNED,\
                                 PRIMARY KEY(id)\
                                 ) ENGINE = InnoDB"
    sql_dtable_products = "DROP TABLE IF EXISTS Products"
    sql_ctable_products = "CREATE TABLE Products (\
                               id INT UNSIGNED AUTO_INCREMENT,\
                               name_product VARCHAR(200) NOT NULL,\
                               brand VARCHAR(200) DEFAULT NULL,\
                               quantity VARCHAR(20) DEFAULT NULL,\
                               nutrition VARCHAR(2) DEFAULT NULL,\
                               description VARCHAR(200) DEFAULT NULL,\
                               url VARCHAR(200) DEFAULT NULL,\
                               code BIGINT UNSIGNED,\
                               PRIMARY KEY(id)\
                               ) ENGINE = InnoDB"
    sql_dtable_product_category = "DROP TABLE IF EXISTS Product_category"
    sql_ctable_product_category = "CREATE TABLE Product_category (\
                                       name_category_fr_b VARCHAR(200),\
                                       name_product_b VARCHAR(200)\
                                       ) ENGINE = InnoDB"
    sql_atables_fk = """ALTER TABLE Product_category
                          ADD CONSTRAINT fk_name_category_fr 
                              FOREIGN KEY (name_category_fr_b) 
                              REFERENCES Categories(name_category_fr),
                          ADD CONSTRAINT fk_products_b 
                              FOREIGN KEY (name_product_b) 
                              REFERENCES Products(name_product)"""
    sql_index_category = "CREATE UNIQUE INDEX unique_category\
                               ON Categories(name_category)"
    sql_index_product = "CREATE UNIQUE INDEX unique_product\
                             ON Products(name_product, brand, quantity)"
#CREATE TABLE saves (
#    id INT UNSIGNED AUTO_INCREMENT,
#    saved_product_id INT UNSIGNED,
#    PRIMARY KEY(id)
#)
#ENGINE=InnoDB;#
#
#CREATE UNIQUE INDEX unique_saves ON Saves(saved_product_id);
    connection = db_connect()

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_dtable_product_category)
            cursor.execute(sql_ctable_product_category)
            cursor.execute(sql_dtable_categories)
            cursor.execute(sql_ctable_categories)
            cursor.execute(sql_dtable_products)
            cursor.execute(sql_ctable_products)
            #cursor.execute(sql_atables_fk )
            cursor.execute(sql_index_product)
            cursor.execute(sql_index_category)
    finally:
    	pass

    connection.commit()
    connection.close()  
    

def db_data_push():
    """ Function that retrieves json from the OFF API and push data to the database
    """
    connection1 = db_connect()
    # retrieve data 
    raw_json_categories_data = requests.get('https://fr.openfoodfacts.org/categories.json')
    categories_data = raw_json_categories_data.json()
    categories_nb = categories_data['count']
    categories_list = categories_data['tags']##    

    # Cycle the list and update Categorie table
    for cat_num in range(1736, 1738):
        category = categories_list[cat_num]
        products_total = category.get('products')
        three_tuples = (category.get('name'), \
                        category.get('id'), \
                        products_total)
        push_data_categories(connection1, three_tuples)
        category_url = category.get('url')
        products_page_total = int(math.ceil(products_total/20))
        print("Je charge les produits de la categorie {}".format(cat_num + 1)) 
        # For each categorie, browses through the pages of 20 products in that category
        for product_page in range(products_page_total):
            products_url = str("{}/{}.json".format(category_url, product_page + 1))
            raw_json_data_products = requests.get(products_url)
            products_data = raw_json_data_products.json()
            products_list = products_data['products']
            products_list_size = len(products_list)
            #print("page {} sur {}".format(product_page, products_page_total))
            # for each product in the list, retrieves the subdata
            for product_num in range(products_list_size):
                products_item = products_list[product_num]
                # Some products have no brand_tags, could use pop or get methods 
                # to override errors and set a default value.
                try:
                    brand_special = str('-'.join(products_item.get('brands_tags')))
                except TypeError:
                    print("Erreur sur {}".format(products_item.get('product_name')))
                    brand_special = "NULL";
                finally:
                    prod_tuples = (products_item.get('product_name'),\
                                brand_special,\
                                products_item.get('quantity'),\
                                products_item.get('nutrition_grades'),\
                                products_item.get('generic_name_fr'),\
                                products_item.get('url'),
                                products_item.get('code'))
                    prod_cat_tuples = (category.get('name'), products_item.get('product_name'))
                    push_data_products(connection1, prod_tuples)
                    push_data_product_category(connection1, prod_cat_tuples)
            connection1.commit()
    connection1.close()

def push_data_categories(connection, three_tuples):
    """ Push data in the categories table
    """
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT IGNORE INTO `Categories` \
               (`name_category_fr`, `name_category`, `nb_products`) \
               VALUES (%s, %s, %s)"
        cursor.execute(sql, three_tuples)

def push_data_products(connection, prod_tuples):
    """ Push data in the products table
    """
    with connection.cursor() as cursor:
    # Create a new record
        sql = "INSERT IGNORE INTO `Products` \
               (`name_product`, `brand`, `quantity`, `nutrition`, `description`, `url`, `code`) \
               VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, prod_tuples)

def push_data_product_category(connection, prod_cat_tuples):
    """ Push data in the product_category table
    """
    with connection.cursor() as cursor:
        sql = "INSERT IGNORE INTO `Product_category` \
               (`name_category_fr_b`, `name_product_b`) \
               VALUES (%s, %s)"
        cursor.execute(sql, prod_cat_tuples)


def main():
    # Commented off the table initiator
    #print(datetime.datetime.now())
    #db_init()
    db_data_push()
    print(datetime.datetime.now())


if __name__ == "__main__":
    main()



