import sqlite3

from shopping import _display_options

def display_orders_history(db, cursor, shopper_id):
    order_query= """ 
    SELECT so.order_id,
        order_date,
        p.product_description,
        s.seller_name,
        PRINTF("£%0.2f", op.price),
        op.quantity,
        op.ordered_product_status
        FROM shopper_orders so
        INNER JOIN
        ordered_products op ON op.order_id = so.order_id
        INNER JOIN   product_sellers AS PS ON ps.product_id = op.product_id 
                                        AND ps.seller_id = op.seller_id
        INNER JOIN products p ON p.product_id = ps.product_id
        INNER JOIN sellers s ON s.seller_id = ps.seller_id
        WHERE so.shopper_id = ?
        GROUP BY so.order_id, op.product_id
        ORDER BY so.order_date DESC"""
    cursor.execute(order_query, (shopper_id,))
    history = cursor.fetchall()
    if history:
        print(" {0:10}   {1:10}   {2:68}    {3:20}  {4:10}   {5:10}    {6:10} ".format(
        "Order ID", "Order Date", "Product Description", "Seller", "Price" ,"Quantity", "Status"))
        for row in history:
            print("{0:10}    {1:10}   {2:72} {3:17}  {4:10} {5:10}      {6:15} ".format(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6] ))
    else:
        print("You have not placed any orders yet")

    


# display_orders_history(10000)   
if __name__ == "__main__":
    
    pass
