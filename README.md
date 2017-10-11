# OC_project_5_OFF

## Objectives
- [] Collect data from openfoodfacts via the site API,
- [] Format them in a MySQL database
- [] Code a program in Python that will allow user to interact with the database

## Requirements
- [] Set up a working environment using Agile tools
- [] Analyze the project specifications 
- [] Identify the data schema for the database
- [] List specifications for the program

# Data collection with Python script
- [] Requests the API to list all the categories
- [] For each category, collects name of the category in french, name of the category in other language, total number of associated products
- [] calculates total number of pages of products associated to the category
- [] For each page, requests the page products (up to 20 per page) and collects name of the product, brand, quantity, barcode entry, decription via its generic name and the url to the product page
- [] populates all three local database tables on the MySQL server: categories, products and product\_category (table that lists per category id, the products associated).
- [] Script ignores brands that are not present (and default the value to NULL) in JSON colleted data and allows for name of product filled in with " "

# UX Python program to request the database 
- [] Select functions for program features, categories, products, recommandations, saved recommandations
- [] Classes and methods for pages of results : pages for categories, products, recommandations and saved recommandations
- [] database functions that collects data from the database : categories, products per category, best similar products, saved recommandations
- [] database function that saves chosen recommandation to the database

