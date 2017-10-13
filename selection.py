#! /usr/bin/env python3
# #-*- coding: utf-8 -*-

import database as db
import menu_browsing as menu

############################
# Menu classes and methods #
############################
""" Module that manages menus for navigation in the application
"""

class MenuCategories():
    """ Menu class for pages of categories
    """
    MAX_LIST_SIZE = menu.PageCategories.OFFSET

    def __init__(self, text_option):
        """ Class initializer
        """
        self.text_option = text_option
        self.page_index = []
        self.data_dict = {1: 'name_category_fr'}
        self.coord = []
        self.max_page_number = 0
        print(self.text_option['loading'])

    def calls_cat_index(self):
        """ Method that populates the index of category pages
        """
        menu.PageCategories.initiates_index()
        self.pages_index = menu.PageCategories.CAT_PAGES_INDEX
        self.max_page_number = len(self.pages_index)

    def displays_page_content(self, page):
        """ Method that displays the content of a page
        """
        print("\nPlease enter a number to make a selection:\n")
        # Using len(), because last page may have less items
        for i in range(len(page.entries_list)):
            # entries_list is a list of dictionnary of dictionnaries, hence
            # the get function and default values to either None and ''
            # as these will not return error but default value if key is missing
            print("{} - {} {} {}".format(i + 1, \
                page.entries_list[i].get(self.data_dict.get(1, None), ''), \
                page.entries_list[i].get(self.data_dict.get(2, None), ''), \
                page.entries_list[i].get(self.data_dict.get(3, None), '')))

    def entry_selection(self):
        """ Method that allows to navigate menus and display page content
        for selection
        Returns a dictionnary if a selection is confirmed
        """
        selection_active = 1
        index_number = 0
        print(self.text_option['index'].format(self.max_page_number))
        while selection_active == 1:
            print(self.text_option['index_position'].format(index_number + 1, \
                                                            self.max_page_number))
            print(self.text_option['index_sorting'])
            page = self.pages_index[index_number]
            self.displays_page_content(page)
            print(self.text_option['navigation_instruction'])
            user_input = input("Type your choice and press 'Enter' key: ")
            valid_numbered_input = map(str, range(1, self.MAX_LIST_SIZE + 1))
            if str.lower(user_input) in valid_numbered_input:
                # returns a dictionnary
                return self.pages_index[index_number].entries_list[int(user_input) - 1]
            elif str.lower(user_input) == 'e':
                selection_active = 0
            elif str.lower(user_input) == 'j':
                selection_temp_active = 1
                while selection_temp_active == 1:
                    user_input_index = input("please enter a page index number: ")
                    valid_numbered_input_index = map(str, \
                                                     range(1, self.max_page_number + 1))
                    if str.lower(user_input_index) in valid_numbered_input_index:
                        index_number = int(user_input_index) - 1
                        selection_temp_active = 0
                    elif str.lower(user_input_index) == 'f':
                        selection_temp_active = 0
                    else:
                        print("""WARNING invalid input,
                              please enter a valid number or 'F' to exit""")
            elif str.lower(user_input) == 'n':
                index_number += 1
            elif str.lower(user_input) == 'p':
                index_number -= 1
            else:
                print(self.text_option['input_error'].format(self.MAX_LIST_SIZE))

    def view_detailed_info(self, recommandation_dict):
        """ Method that displays more details on the recommandation
        """
        rc = recommandation_dict
        rc_name = rc['name_product']
        rc_brand = rc['brand']
        rc_quantity = rc['quantity']
        rc_description = rc['description']
        rc_nutrition = rc['nutrition'].capitalize()
        rc_url = rc['url']
        print(self.text_option['item_display'].format(rc_name,\
                                                      rc_brand,\
                                                      rc_quantity,\
                                                      rc_description,\
                                                      rc_nutrition,\
                                                      rc_url))
        input("Press any key to continue")


class MenuProducts(MenuCategories):
    """ Menu class for pages of products
    Based on category selected by user
    """
    def __init__(self, text_option, category_selected):
        """ Class initializer
        """
        super().__init__(text_option)
        self.data_dict = {1: 'name_product', 2: 'brand', 3: 'quantity'}
        # Category selected is a string
        self.category_selected = category_selected

    def calls_prod_index(self):
        """ Method that populates the index of product pages
        """
        menu.PageProducts.initiates_prod_index(self.category_selected)
        self.pages_index = menu.PageProducts.PROD_PER_CAT_PAGES_INDEX
        self.max_page_number = len(self.pages_index)


class MenuRecommandations(MenuProducts):
    """ Menu class for pages of recommandations
    Based on category selected and product selected by user
    """
    def __init__(self, text_option, category_selected, product_selected_dict):
        """ Class initializer
        """
        super().__init__(text_option, category_selected)
        # product selected is a dict
        ps_name = product_selected_dict['name_product']
        ps_brand = product_selected_dict['brand']
        ps_quantity = product_selected_dict['quantity']
        self.pages_index = [menu.PageRecommandation(self.category_selected, \
                                                     ps_name, \
                                                     ps_brand, \
                                                     ps_quantity)]

    def save_proposal(self, recommandation_dict):
        """ Method offers user to save his selection
        """
        selection_active = 1
        print(self.text_option['save_proposal'])
        while selection_active == 1:
            user_input = input("Yes / No: ")
            if str.lower(user_input) in 'yes':
                db.push_saves(recommandation_dict)
                selection_active = 0
            elif str.lower(user_input) in 'no':
                selection_active = 0
            else:
                print("save_input_error")


class MenuSaves(MenuCategories):
    """ Menu class for pages of saved recommandations
    Based on category selected and product selected by user
    """
    def __init__(self, text_option):
        """ Class initializer
        """
        super().__init__(text_option)
        self.data_dict = {1: 'name_product', 2: 'brand', 3: 'quantity'}

    def calls_saves_index(self):
        """ Method that populates the index of saved recommandations
        """
        menu.PageSaves.initiates_saves_index()
        self.pages_index = menu.PageSaves.SAVES_PAGES_INDEX
        self.max_page_number = len(self.pages_index)
