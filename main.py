#! /usr/bin/env python3
# #-*- coding: utf-8 -*-

#################
# Main function #
#################
""" Main script for the Open Food Facts database explorer
"""

# Import menu selection module
import json
import selection as select


def menu_start_up(text_features):
    """ Loads menu text options
    Loads start up features selection menu
    """
    print(text_features['opening'])
    print(text_features['main_options'])
    print(text_features['exit_option'])

def main():
    """ Main function calling on selection menus for UX
    """
    # User interface texts loading
    text = json.load(open("menu_text.json"))
    text_features = text['features']
    text_categories = text['categories']
    text_products = text['products']
    text_recommandations = text['recommandations']
    text_saves = text['saves']
    # Initial loading phase to load pages of categories
    menu_categories = select.MenuCategories(text_categories)
    menu_categories.calls_cat_index()
    programme_active = 1
    while programme_active == 1:
        # Initial menu, presenting options for programme features
        menu_start_up(text_features)
        selection = input("Please make a selection : ")
        if str(selection) == '1':
            # UX menu for category selection and
            # returns dict if a category is selected
            result_cat_select_dict = menu_categories.entry_selection()
            if not result_cat_select_dict:
                # Case when exiting category selection
                selection = 0
            else:
                category_selected = result_cat_select_dict['name_category_fr']
                # Products pages loading
                menu_products = select.MenuProducts(text_products, \
                                                     category_selected)
                menu_products.calls_prod_index()
                # UX menu for product selection and
                # returns dict if a product is selected
                result_prod_select_dict = menu_products.entry_selection()
                if not result_prod_select_dict:
                    selection = 0
                else:
                    product_selected_dict = result_prod_select_dict
                    # Recommandations page loading
                    menu_recommandations = select.MenuRecommandations(
                        text_recommandations, \
                        category_selected, \
                        product_selected_dict)
                    # UX menu for recommandation selection
                    # returns the dictionnary with all the recommandation data
                    result_rec_select_dict = menu_recommandations.entry_selection()
                    if not result_rec_select_dict:
                        selection = 0
                    else:
                        recommandation_selected_dict = result_rec_select_dict
                        # Displays detailed info on recommandation selected
                        menu_recommandations.view_detailed_info(recommandation_selected_dict)
                        # offers to save selection for later viewing
                        menu_recommandations.save_proposal(recommandation_selected_dict)
        elif str(selection) == '2':
            # UX menu for saved recommandation and
            # allows to display recommandation detailed info
            menu_saves = select.MenuSaves(text_saves)
            menu_saves.calls_saves_index()
            save_selected_dict = menu_saves.entry_selection()
            menu_saves.view_detailed_info(save_selected_dict)
        elif str.lower(selection) == 'f':
            # farewell message, cause we aren't savages
            print("\n\nSee you soon and have a nice day !\n\n")
            programme_active = 0
        else:
            # warning notification for incorrect input
            print("\nSorry, please verify your entry :)\n")


if __name__ == "__main__":
    main()
