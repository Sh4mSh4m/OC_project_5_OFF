# OC_project_5_OFF

## Objectives
- [x] Collect data from openfoodfacts via the site API,
- [x] Format them in a MySQL database
- [x] Code a program in Python that will allow user to interact with the database

## Requirements
- [x] Set up a working environment using Agile tools
- [x] Analyze the project specifications 
- [x] Identify the data schema for the database
- [x] List specifications for the program

# Data collection with Python script
- [x] Requests the API to list all the categories
- [x] For each category, collects name of the category in french, name of the category in other language, total number of associated products
- [x] calculates total number of pages of products associated to the category
- [x] For each page, requests the page products (up to 20 per page) and collects name of the product, brand, quantity, barcode entry, decription via its generic name and the url to the product page
- [x] populates all three local database tables on the MySQL server: categories, products and product\_category (table that lists per category id, the products associated).
- [x] Script ignores brands that are not present (and default the value to NULL) in JSON colleted data and allows for name of product filled in with " "

# UX Python program to request the database 
- [x] Classes and methods for menus of selection. Navigation options to jump to next or previous page or enter an index page to go straight to it. Also allows to exit and come back to initial menu of features.
- [x] Classes and methods for pages of results : pages for categories, products, recommandations and saved recommandations
- [x] database functions that collects data from the database : categories, products per category, best similar products, saved recommandations
- [x] database function that saves chosen recommandation to the database

