import database as db
import menu_browsing as menu

def features():
    print("Welcome to the Nutritious Food replacement program !")
    print("Search a product in the Open Food Facts, please make a selection:")
    print("\n1 - Lookup categories")
    print("2 - Lookup saved recommandations\n")
    print("\nEnter F to exit program\n")

def categories():
    selection_active = 1
    index_number = 0
    max_list_size = menu.Page_categories.OFFSET
    print("\nCategories list loading...\n")
    menu.Page_categories.initiates_index()
    cat_pages_index = menu.Page_categories.CAT_PAGES_INDEX
    max_page_number = len(cat_pages_index)
    print("\nThanks for waiting, there are {} pages of categories".format(max_page_number))

    while selection_active == 1:
        print("\n\n\nYou are currently browsing page {} out of {}".format(index_number + 1, max_page_number))
        print("Categories are ordered from largest to smallest categories")
        cat_page = cat_pages_index[index_number] 
        cat_page.displays_categories()
        print("Enter a number from 1 to 10 to select a category")
        print("Enter 'j' to jump to another page of result ")
        print("Enter 'e' to exit")
        print("Enter 'n' to go to the next page")
        user_input = input("Type your choice and press 'Enter' key: ")
        valid_numbered_input = map(str, range(1, max_list_size + 1))
        if str.lower(user_input) in valid_numbered_input:
            category_selected = cat_page.entries_list[int(user_input) - 1]['name_category_fr']
            # Returns string
            return category_selected
            selection_active = 0
        elif str.lower(user_input) == 'f':
            selection_active = 0
        elif str.lower(user_input) == 'n':
            index_number += 1
        else:
            print("Please enter a number from 1 to {}, E, J ou N".format(max_list_size))

def products(category_selected):
    selection_active = 1
    index_number = 0 
    max_list_size = menu.Page_categories.OFFSET
    print("\nProducts list loading...\n")
    menu.Page_products.initiates_prod_index(category_selected)
    prod_per_cat_pages_index = menu.Page_products.PROD_PER_CAT_PAGES_INDEX
    max_page_number = len(prod_per_cat_pages_index)
    print("\nThanks for waiting, there are {} pages of products".format(max_page_number))

    while selection_active == 1:
        print(category_selected)
        print("\n\n\nYou are currently browsing page {} out of {}".format(index_number + 1, max_page_number))
        print("Products are ordered by alphabetical order")
        prod_per_cat_page = prod_per_cat_pages_index[index_number] 
        prod_per_cat_page.displays_products()
        print("Enter a number from 1 to 10 to select a category")
        print("Enter 'j' to jump to another page of result ")
        print("Enter 'e' to exit")
        print("Enter 'n' to go to the next page")
        user_input = input("Type your choice and press 'Enter' key: ")
        valid_numbered_input = map(str, range(1, max_list_size + 1))
        if str.lower(user_input) in valid_numbered_input:
            p_data = prod_per_cat_page.entries_list[int(user_input) - 1]
            product_selected = str(p_data['name_product']) + '%'#,p_data['brand'], p_data['quantity'], p_data['nutrition']) 
            print(product_selected)
            return product_selected
            selection_active = 0
        elif str.lower(user_input) == 'e':
            selection_active = 0
        elif str.lower(user_input) == 'n':
            index_number += 1
        else:
            print("Please enter a number from 1 to {}, E, J ou N".format(max_list_size))
        break

def view_saved_recommandations():
    selection_active = 1
    index_number = 0
    max_list_size = menu.Page_categories.OFFSET
    print("\nSaves loading...\n")
    menu.Page_saves.initiates_saves_index()
    saves_pages_index = menu.Page_saves.SAVES_PAGES_INDEX
    max_page_number = len(saves_pages_index)
    print("\nThanks for waiting, there are {} pages of saves".format(max_page_number))

    while selection_active == 1:
        print("\n\n\nYou are currently browsing page {} out of {}".format(index_number + 1, max_page_number))
        print("Products are ordered by alphabetical order")
        saves_page = saves_pages_index[index_number] 
        saves_page.displays_saves()
        print("Enter a number from 1 to 10 to select a category")
        print("Enter 'j' to jump to another page of result ")
        print("Enter 'e' to exit")
        print("Enter 'n' to go to the next page")
        user_input = input("Type your choice and press 'Enter' key: ")
        valid_numbered_input = map(str, range(1, max_list_size + 1))
        if str.lower(user_input) in valid_numbered_input:
            saves_data = saves_page.entries_list[int(user_input) - 1]
            print("\nProduct details :\n")
            print("Name: {} {} {}".format(saves_data['name_product'], saves_data['brand'], saves_data['quantity']))
            print("Description: {}".format(saves_data['description']))
            print("Web link: {}".format(saves_data['url']))
            selection_active = 0
        elif str.lower(user_input) == 'e':
            selection_active = 0
        elif str.lower(user_input) == 'n':
            index_number += 1
        else:
            print("Please enter a number from 1 to {}, E, J ou N".format(max_list_size))
        break

def recommandations(name_category_fr, product_selected):
    selection_active = 1
    print("\nRecommandation loading...\n")
    max_list_size = menu.Page_categories.OFFSET
    while selection_active == 1:
        recommandation_page = menu.Page_recommandation(name_category_fr, product_selected)
        #print(recommandation_page.entries_list)
        recommandation_page.displays_recommandations()
        print("Enter a number from 1 to 10 to select a category")
        print("Enter 'e' to exit")
        user_input = input("Type your choice and press 'Enter' key: ")
        valid_numbered_input = map(str, range(1, max_list_size + 1))
        if str.lower(user_input) in valid_numbered_input:
            recommandation_dict = recommandation_page.entries_list[int(user_input) - 1]
            print(recommandation_dict)
            return recommandation_dict
            selection_active = 0
        elif str.lower(user_input) == 'e':
            selection_active = 0
        else:
            print("Please enter a number from 1 to {}, E, J ou N".format(max_list_size))
        break
    
def save(recommandation_dict):
    selection_active = 1
    while selection_active == 1:
        user_input = input("Yes / No: ")
        if str.lower(user_input) in 'yes':
            db.push_saves(recommandation_dict)
            selection_active = 0
        elif str.lower(user_input) in 'no':
            selection_active = 0
        else:
            print("Please enter yes or no")

