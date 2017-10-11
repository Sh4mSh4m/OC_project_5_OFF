#! /usr/bin/env python3
# #-*- coding: utf-8 -*-

# Import menu selection module
import selection as select

def main():
    """ Main function calling on selection menus for UX 
    """
    programme_active = 1
    while programme_active == 1:
        # initial menu, presenting options for programme features
        select.features()
        selection = input("Type your choice and press 'Enter' key: ")
        # product research feature
        if str(selection) == '1':
            # UX menu for category selection and 
            # returns string for name_category_fr selected
            category_selected = select.categories()
            # UX menu for product selection and 
            # returns string for name_product selected with '%' added
            # for string comparison in the MySQL request
            product_selected = select.products(category_selected)
            # UX menu for recommandation selection
            # returns the dictionnary with all the recommandation data
            recommandation = select.recommandations(category_selected, 
                                                    product_selected)
            # offers to save selection for later viewing
            select.save(recommandation)
        # saved recommandation lookup
        elif str(selection) == '2':
            # UX menu for saved recommandation and
            # allows to display recommandation detailed info
            select.view_saved_recommandations()
        # exit the program properly
        elif str.lower(selection) == 'f':
            # farewell message, cause we aren't savages
            print("\n\nSee you soon and have a nice day !\n\n")
            programme_active = 0
        # 
        else:
            # warning notification for incorrect input
            print("\nSorry, please verify your entry :)\n")

if __name__ == "__main__":
    main()


