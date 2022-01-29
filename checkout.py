import datetime
from shopping import _display_options, execute_query, if_null
from clear_basket import clear_basket


def checkout(db, cursor, shopper_id):
    # IFNULL(delivery_address_line_1,"Null"), IFNULL(delivery_address_line_2,"Null"),
    #   IFNULL(delivery_address_line_3,"Null")

    checkout_query = """ 
                SELECT  so.delivery_address_id, delivery_address_line_1,
                 delivery_address_line_2,  delivery_address_line_3
                FROM shopper_delivery_addresses da
                INNER JOIN shopper_orders so ON so.delivery_address_id 
                = da.delivery_address_id
                WHERE shopper_id = ?
                GROUP BY so.delivery_address_id
                ORDER BY order_date DESC
                """

    addresses = execute_query(cursor, checkout_query, shopper_id)

    if addresses:
        # acticate the address option to display properly
        selected_address = _display_options(
            addresses, "Addresses", "address", address=True)
        address_id = addresses[selected_address][0]
    else:  # if not addresses exist, create a new address
        print("Add an address")
        address_line_1 = input("\nEnter the delivery address line 1: ")
        address_line_2 = input("\nEnter the delivery address line 2: ")
        address_line_3 = input("\nEnter the delivery address line 3: ")
        country = input("\nEnter the delivery country: ")
        post_code = input("\nEnter the delivery post code: ")

        insert_address_query = """INSERT INTO shopper_delivery_addresses (
            delivery_address_line_1, delivery_address_line_2, delivery_address_line_3,
                                    delivery_county, delivery_post_code)
                                    VALUES(?, ?, ?, ?, ?)
                                """

        cursor.execute(insert_address_query, (address_line_1,
                       address_line_2, address_line_3, country, post_code))
        db.commit()
        print("Address added successfully")

        # Get the id of the last added address
        last_addred_address_query = """ 
                                     SELECT  delivery_address_id, 
                                     delivery_address_line_1, delivery_address_line_2,
                                     delivery_address_line_3
                                    FROM shopper_delivery_addresses da
                                    ORDER BY delivery_address_id DESC
                                    LIMIT 1
                                    """
        cursor.execute(
            last_addred_address_query)  # return the last added address
        address = cursor.fetchone()
        address_id = address[0]

    card_query = """        
    SELECT spc.payment_card_id, card_type, card_number
    FROM shopper_payment_cards spc
    INNER JOIN shopper_orders so ON so.payment_card_id = spc.payment_card_id
    WHERE so.shopper_id = ?
    GROUP BY spc.payment_card_id"""

    cards = execute_query(cursor, card_query, shopper_id)
    # print(cards)

    # print(cards)
    if cards:  # if there is no saved cards, insert a new card
        # acticate the checkout option to display properly
        selected_card_id = _display_options(
            cards, "Checkout cards", "card", checkout=True)
        card_id = cards[selected_card_id][0]
    else:
        print("You need to add a card to checkout")
        type = ["Visa", "Mastercard", "AMEX"]
        display_cards = _display_options(type, "Cards type", "card")
        selected_card = type[display_cards]
        # Add a new card
        card_number = 0
        while card_number == 0 or len(str(card_number)) != 16:
            card_number = input(
                f"Enter the {selected_card} number (16 digits)")

        last_card_query = """
                            SELECT  payment_card_id 
                                    FROM shopper_payment_cards 
                                    ORDER BY payment_card_id DESC
                                    LIMIT 1
                            """
        card = execute_query(cursor, last_card_query,
                             fetch=1)  # return the last card id

        # get the next card id, if null, mean this is first card to be inserted 
        # in DB and assign the id to 1

        card_id = if_null(card)

        insert_card_query = """
                            INSERT INTO shopper_payment_cards(payment_card_id, 
                            card_type, card_number)
                            VALUES(?, ?, ?)
                                """
        cursor.execute(insert_card_query,
                       (card_id, selected_card, card_number,))
        db.commit()
        print("Card added successfully")

    curr_date = datetime.date.today().strftime("%Y-%m-%d")
    # print(shopper_id, address_id, card_id, curr_date, "Placed")

    last_shoper_order_query = """
                    SELECT order_id FROM  shopper_orders so
                    INNER JOIN shoppers s ON s.shopper_id = so.shopper_id
                    ORDER BY order_id DESC
                    LIMIT 1
                    """

    last_order_id = execute_query(cursor, last_shoper_order_query,  fetch=1)
    # print(last_order_id[0])
    next_order_id = if_null(last_order_id)

    shopper_order_query = """
                        INSERT INTO shopper_orders(order_id, shopper_id, 
                        delivery_address_id, payment_card_id, order_date, order_status)
                        VALUES (?,?, ?, ?, ?, ?)
                    """
    cursor.execute(shopper_order_query, (next_order_id,
                   shopper_id, address_id, card_id, curr_date, "Placed"))
    db.commit()
    # Create ordered product table for each product in the cart
    cart_date_query = """
                        SELECT  product_id, seller_id, quantity, price
                        FROM basket_contents bc
                        INNER JOIN shopper_baskets  sb ON sb.basket_id = bc.basket_id
                        WHERE sb.shopper_id = ?
                        """

    cart_data = execute_query(cursor, cart_date_query, shopper_id)

    # Create ordered_products table for each product
    if cart_data:
        for cart in cart_data:
            # print(cart)
            order_id = next_order_id
            product_id = cart[0]
            seller_id = cart[1]
            quantity = cart[2]
            price = cart[3]
            product_statud = "Placed"
            ordered_products_query = """
                                INSERT INTO ordered_products(order_id,
                                 product_id, seller_id, quantity, price, 
                                 ordered_product_status)
                                VALUES (?, ?, ?, ?, ?,?)
                            """
            cursor.execute(ordered_products_query, (order_id, product_id,
                           seller_id, quantity, price, product_statud,))
            db.commit()

        print("Order has been placed")

        # clear the basker after order is placed
        clear_basket(cursor, db, shopper_id)


if __name__ == "__main__":

    pass
