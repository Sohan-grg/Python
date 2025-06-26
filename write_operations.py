def save_product_data(product_dict):
    """
    Saves product data to products.txt
    """
    try:
        data_file = open("products.txt", "w")
        for product_id, product in product_dict.items():
            line = (
                product['name'] + "," +
                product['brand'] + "," +
                str(product['quantity']) + "," +
                str(product['price']) + "," +
                product['origin'] + "\n"
            )
            data_file.write(line)
        data_file.close()
    except IOError:
        print("Error occurred while saving product data.")

def create_invoice_file(file_name, content):
    """
    Creates an invoice file with given content
    """
    try:
        invoice_file = open(file_name, "w")
        invoice_file.write(content)
        invoice_file.close()
        return True
    except IOError:
        print("Error occurred while creating invoice file.")
        return False
