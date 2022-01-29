import sqlite3
import sys

import basket
import checkout
import display_orders 
import shopping


def main():
    try:
       
        db = sqlite3.connect("Orinoco")  #Connect to the database
        cursor = db.cursor()
        print("Successfully connected to Orinoco database\n")
        shopper_exist = 0
        user_id = 1


        #Fetch the shopper id
        while not shopper_exist: 
            try:
                user_id = int(input("Enter your shopping ID or 0 to exit: "))
                if user_id == 0:
                    db.close()
                    sys.exit()
                #search the user ID in the DB
                search_query = "SELECT * FROM shoppers WHERE shopper_id = ?"
                shopper_exist = shopping.execute_query(cursor, search_query,user_id,  fetch= 1)
                if not shopper_exist:
                    print(" No user with this id")
            except ValueError :
                print("This user ID doesn't exist, try again...")


        if shopper_exist:
            first_name = shopper_exist[2]
            last_name =  shopper_exist[3]

            print("\nWelcome {0} {1}".format(first_name, last_name))
            
            while True:
                options = ["Display your order history", "Add an item to your basket" 
                            ,  "View your basket", "Checkout", "Exit"]
                choice = shopping._display_options(options, "Menu", "function") #returned choid is minus one
                # print(choice)

                #Decision making based on user choice
                if choice == 0:
                    display_orders.display_orders_history(db, cursor, user_id)
                elif choice ==1:   
                    shopping.add_to_user_basket(db, cursor, user_id)
                elif choice == 2:
                    basket.show_basket(cursor, user_id)
                elif choice ==3:
                    check_basket = basket.show_basket(cursor, user_id) #check if there are products in the basket, if True, continue with checkout.checkout
                    if check_basket:
                        checkout.checkout(db, cursor, user_id)
                elif choice == 4:
                    db.close()
                    sys.exit("\nThank you for shopping with Orinoco LTD!")                   

        else:
            print(f"Sorry, the following shopping ID [{user_id}] doesn't exit")
            db.close()

        db.close()

    except Exception as e:
        print("Invalid input or DB error")
        db.close()
        print(e)
    

if __name__ == "__main__":
    print()
    main()
