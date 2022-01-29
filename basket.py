from shopping import execute_query


def show_basket(cursor, shopper_id):
    show_basket_query = """
            SELECT p.product_description, s.seller_name, bc.quantity, bc.price AS Price, bc.quantity*bc.price AS Total
            FROM basket_contents bc
            INNER JOIN shopper_baskets sb ON sb.basket_id = bc.basket_id
            INNER JOIN product_sellers ps ON ps.product_id = bc.product_id AND ps.seller_id = bc.seller_id
            INNER JOIN products p ON p.product_id = ps.product_id
            INNER JOIN sellers s ON s.seller_id = ps.seller_id
            WHERE sb.shopper_id = ?
            """
    show_basket = execute_query(cursor, show_basket_query, (shopper_id))
    sum = 0
    if show_basket:
        print(" {0:50}    {1:23}       {2:10}      {3:10}  {4:7}".format("Product \
         Description", "Seller_name", "Quantiy", "Price", "Total"))

        for row in show_basket:
            product_description = row[0]
            if len(product_description) > 50:
                product_description1 = product_description.split(', ')[0]
                product_description2 = product_description.split(', ')[1:]
                product_description2 = ' '.join(product_description2)

                print(" {0:50}    {1:23}   {2:10}         {3:7.2f}    {4:7.2f}".format(\
                    product_description1, row[1], row[2], row[3], row[4]))
                print(f" {product_description2}")
            else:
                print(" {0:50}    {1:23}   {2:10}         {3:7.2f}    {4:7.2f}".format(\
                     row[0], row[1], row[2], row[3], row[4]))

            sum += row[4]
        print("\n\t\t\t\t{0:66}Basket Total:  £{1:7.2f}".format(" ", sum))
        return True
    else:
        print("\nBasket is Empty\n")
        return False


if __name__ == "__main__":
    pass
    # import sqlite3
    # db = sqlite3.connect("Orinoco")
    # cursor = db.cursor()
    # show_basket(cursor, 10000)
