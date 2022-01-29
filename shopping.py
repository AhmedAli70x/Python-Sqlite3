import datetime



def execute_query(cursor, query, *args, fetch=None):
    cursor.execute(query, (args))
    if fetch == 1:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    return(result)


def _display_options(all_options, title, type, sellers=False,  address=False, checkout=False):
    options_number = len(all_options)
    print("\n", title)
    print("--------------\n")

    if sellers:
        for option in range(options_number):
            print("{0}. {1:18} £{2:4.2f}".format((option+1),
                  all_options[option][1], all_options[option][2]))

    elif checkout:
        for card in range(options_number):
            print("{0}.  {1}  ends with *{2} ".format(card+1,
                  all_options[card][1], all_options[card][2][-4:]))
    elif address:
        for addr in range(options_number):
            print("{0}.  {1}, {2} ,{3} ".format(
                addr+1, all_options[addr][1], all_options[addr][2] or " ", all_options[addr][3] or " "))

    else:
        for option in range(options_number):
            print("{0}. {1:20} ".format((option+1), all_options[option]))

    selected_option = 0
    while selected_option > options_number or selected_option == 0:
        prompt = "Enter the number against the "+type+" you want to choose: "

        while True:
            try:
                selected_option = int(input(prompt))
                break
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")

    return (selected_option-1)


def return_list(data, index, addr=False):
    if data and addr:
        mylist = []
        for row in data:
            mylist.append(row[index])
        return mylist
    elif data:
        mylist = []
        for row in data:
            if row[index] not in mylist:
                mylist.append(row[index])
        return mylist
    else:
        print("error")


def if_null(id):
    if id:
        return id[0]+1
    else:
        return 1


def add_to_user_basket(db, cursor, shopper_id):
    product_categories = """ 
                        SELECT category_id, category_description FROM categories
                        """
    
    categories = execute_query(cursor, product_categories)
    if categories:
        categories_list = return_list(categories, 1)
        # print(categories_list)
        slected_category = _display_options(
            categories_list, "Product Categories", "category")
        category_id = categories[slected_category][0]
    # print(category_id)

    # Display products under selected category
    selected_category_products = """
    SELECT product_id, product_description FROM products
        WHERE category_id = ? """
    products = execute_query(cursor, selected_category_products, category_id)

    #return list for the products
    products_list = return_list(products, 1)

    selected_products = _display_options(products_list, "Products", "proudct")
    product_id = products[selected_products][0]
    # print(product_id)

    # Display sellers who sell this product and each price
    product_sellers = """
                    SELECT s.seller_id, seller_name, price
                FROM sellers s
                INNER JOIN product_sellers ps ON ps.seller_id = s.seller_id
                WHERE product_id = ?
                """
    cursor.execute(product_sellers, (product_id,))
    sellers = cursor.fetchall()

    if sellers:
        selected_seller = _display_options(
            sellers, "Sellers", "seller", sellers=True)
        seller_id = sellers[selected_seller][0]
        price = sellers[selected_seller][2]

    else:
        print("No current seller for this product")

    # The quatinty of the selected product
    quantiy = 0
    while True:
        try:
            quantiy = int(input("Enter the quantity you want to buy (min 1- maxsfsdf): "))
            if 9 >= quantiy >= 1:
                break
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

    # get the last basket_id
    shopper_baskets_query = """
                SELECT * FROM shopper_baskets
                ORDER BY basket_id DESC
                limit 1
                """
    basket_id_db = execute_query(cursor, shopper_baskets_query, fetch=1)
    # print('basket_id_db: ', basket_id_db)

    # Increment the basket_id avoid a product to be added to the same basket_id
    basket_id = if_null(basket_id_db)
    # print(basket_id)

    # datetime library to get the current date.
    curr_date = datetime.date.today().strftime("%Y-%m-%d")

    create_basket = """
                    INSERT INTO shopper_baskets(basket_id, shopper_id, basket_created_date_time)
                    VALUES (?, ?, ?)
                    """
    cursor.execute(create_basket, (basket_id, shopper_id, curr_date,))
    db.commit()
    
    print("New basket added")

    basket_content_insert = """
                        INSERT INTO basket_contents(basket_id, product_id, seller_id, quantity, price)
                        VALUES (?, ?, ?, ?, ?)"""

    # print(basket_id, product_id, seller_id, quantiy, price )
    cursor.execute(basket_content_insert, (basket_id,
                   product_id, seller_id, quantiy, price))
    db.commit()
    print("Item added to shoppint cart")

# shopping(10000)


if __name__ == "__main__":
    pass
