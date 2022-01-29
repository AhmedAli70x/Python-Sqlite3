from shopping import execute_query


def clear_basket(cursor, db, shopper_id):

    basket_content_query= """
                        SELECT  bc.basket_id , product_id
                        FROM shopper_baskets sb
                        INNER JOIN basket_contents bc ON sb.basket_id = bc.basket_id
                        WHERE sb.shopper_id =  ?
                        """
    baskets = execute_query(cursor, basket_content_query, shopper_id)
    # print (baskets)
    if baskets:

        # print(baskets)
        
        for basket in baskets:
            #basket content should be cleared first according to sqlite_sequence table
            clear_basket_query = """
                                DELETE from basket_contents
                                WHERE basket_id = ? AND product_id = ?
                                """
            basket_id =  basket[0]
            product_id = basket[1]
            cursor.execute(clear_basket_query, (basket_id,product_id,))
            db.commit()
        # print("basket_shopper  is cleared")

    #this condition for testing
    # else:
    #     print("basket_contents already empty")


        #shopper_baskets should be cleared after basket_content according to
        #  sqlite_sequence table
    basket_shopper_query = """
                            SELECT  basket_id 
                            FROM shopper_baskets 
                              WHERE Shopper_id =  ?
                            """
    basket_shopper = execute_query(cursor, basket_shopper_query, (shopper_id))
    if basket_shopper:
        for basket in basket_shopper:
            
            clear_shopper_baskets = """
                                DELETE from shopper_baskets
                                WHERE basket_id = ? """

            basket_shopper_id = basket[0]

            cursor.execute(clear_shopper_baskets, (basket_shopper_id,))
            db.commit()
        # print("basket_shopper  is cleared")

    #this condition for testing
    # else: 
    #     print("basket_shopper already empty")

    print("Basket cleared")

#Teting the function
# clear_basket(10010)

if __name__ == "__main__":
    
    pass
