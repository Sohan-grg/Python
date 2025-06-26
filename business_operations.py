from datetime import datetime
from write_operations import create_invoice_file
from read_operations import convert_to_float, convert_to_int

def display_product_inventory(product_dict):
    """
    Displays all products in inventory
    """
    print("\n" + create_line(90))
    print(create_header())
    print(create_line(90))
    for product_id, product in product_dict.items():
        print(create_product_row(product_id, product))
    print(create_line(90))

def create_line(length):
    """Creates a line of dashes"""
    return "-" * length

def create_header():
    """Creates inventory display header"""
    return (
        pad_text("ID", 5) +
        pad_text("Name", 25) +
        pad_text("Brand", 15) +
        pad_text("Qty", 10) +
        pad_text("Price", 15) +
        pad_text("Origin", 20)
    )

def pad_text(text, length):
    """Pads text with spaces to specified length"""
    if len(text) >= length:
        return text[:length]
    return text + " " * (length - len(text))

def create_product_row(product_id, product):
    """Creates a formatted product row"""
    selling_price = product['price'] * 2  # Calculate 200% markup
    return (
        pad_text(str(product_id), 5) +
        pad_text(product['name'], 25) +
        pad_text(product['brand'], 15) +
        pad_text(str(product['quantity']), 10) +
        pad_text(str(round(selling_price, 2)), 15) +  # Show selling price
        pad_text(product['origin'], 20)
    )

def process_product_sale(product_dict):
    """
    Handles the product sale process
    """
    customer_name = input("Enter customer name: ")
    customer_phone = input("Enter customer phone: ")
    sale_items = []
    subtotal = 0
    
    while True:
        display_product_inventory(product_dict)
        try:
            product_id = int(input("Enter product ID (0 to finish): "))
            if product_id == 0:
                break
            if product_id not in product_dict:
                print("Invalid product ID!")
                continue
                
            quantity = int(input("Enter quantity to sell: "))
            if quantity <= 0:
                print("Quantity must be positive!")
                continue
                
            free_items = quantity // 3
            if quantity + free_items > product_dict[product_id]['quantity']:
                print("Not enough stock available!")
                continue
                
            product_dict[product_id]['quantity'] -= (quantity + free_items)
            item_total = quantity * product_dict[product_id]['price'] * 2
            subtotal += item_total
            
            item_description = (
                product_dict[product_id]['name'] + " (" + 
                product_dict[product_id]['brand'] + "): " + 
                str(quantity) + " (+" + str(free_items) + ") x " + 
                str(round(product_dict[product_id]['price'] * 2, 2)) + " = " + 
                str(round(item_total, 2))
                )
            sale_items.append(item_description)
        except ValueError:
            print("Invalid input! Please enter numbers only.")
    
    if not sale_items:
        return
    
    shipping_cost = calculate_shipping(subtotal)
    total_amount = subtotal + shipping_cost
    invoice_content = generate_invoice_content(
        "SALE",
        customer_name,
        customer_phone,
        sale_items,
        subtotal,
        shipping_cost,
        total_amount
    )
    
    time_stamp = get_current_time_stamp()
    file_name = "sales_INV-" + time_stamp + ".txt"
    if create_invoice_file(file_name, invoice_content):
        print("Sale invoice saved as " + file_name)
    return product_dict

def calculate_shipping(amount):
    """Calculates shipping cost"""
    return max(100, amount * 0.05)

def generate_invoice_content(invoice_type, name, phone, items, subtotal, shipping, total):
    """Generates invoice content"""
    separator = "=" * 50 + "\n"
    time_stamp = get_current_time_stamp()
    invoice_no = invoice_type + "-" + time_stamp
    
    content = separator
    content += "WECARE INVOICE\n"
    content += "Invoice No: " + invoice_no + "\n"
    content += "Date: " + get_current_date_time() + "\n"
    
    if invoice_type == "SALE":
        content += "Customer: " + name + "\n"
        content += "Phone: " + phone + "\n\n"
    else:
        content += "Supplier: " + name + "\n\n"
    
    content += "\n".join(items) + "\n\n"
    content += "Subtotal: " + str(round(subtotal, 2)) + "\n"
    content += "Shipping: " + str(round(shipping, 2)) + "\n"
    content += "Total: " + str(round(total, 2)) + "\n"
    content += separator + "Thank you!\n"
    return content

def get_current_time_stamp():
    """Generates current timestamp without using strftime"""
    now = datetime.now()
    return (
        str(now.year) + 
        pad_number(now.month) + 
        pad_number(now.day) + "-" +
        pad_number(now.hour) + 
        pad_number(now.minute) + 
        pad_number(now.second)
    )

def pad_number(number):
    """Pads single-digit numbers with leading zero"""
    return "0" + str(number) if number < 10 else str(number)

def get_current_date_time():
    
    now = datetime.now()
    return (
        pad_number(now.day) + "/" +
        pad_number(now.month) + "/" +
        str(now.year) + " " +
        pad_number(now.hour) + ":" +
        pad_number(now.minute) + ":" +
        pad_number(now.second)
    )

def process_product_restock(product_dict):
    """
    Handles the product restocking process
    """
    supplier_name = input("Enter supplier name: ")
    restock_items = []
    total_cost = 0
    
    while True:
        display_product_inventory(product_dict)
        try:
            product_id = int(input("Enter product ID (0 to finish): "))
            if product_id == 0:
                break
            if product_id not in product_dict:
                print("Invalid product ID!")
                continue
                
            quantity = int(input("Enter quantity to restock: "))
            if quantity <= 0:
                print("Quantity must be positive!")
                continue
                
            if get_yes_no_input("Update price (current " + str(product_dict[product_id]['price']) + ")? "):
                while True:  # Add price validation loop
                    try:
                        new_price = float(input("Enter new price: "))
                        if new_price <= 0:
                            print("Price must be positive!")
                            continue
                        product_dict[product_id]['price'] = new_price
                        break
                    except ValueError:
                        print("Invalid price! Please enter a valid number.")
                
            product_dict[product_id]['quantity'] += quantity
            item_cost = quantity * product_dict[product_id]['price']
            total_cost += item_cost
            item_description = (
                product_dict[product_id]['name'] + " (" + 
                product_dict[product_id]['brand'] + "): " + 
                str(quantity) + " @ " + 
                str(product_dict[product_id]['price']) + " = " + 
                str(round(item_cost, 2)))
            restock_items.append(item_description)
        except ValueError:
            print("Invalid input! Please enter numbers only.")
    
    if not restock_items:
        return product_dict
    
    invoice_content = generate_invoice_content(
        "RST",
        supplier_name,
        "",
        restock_items,
        total_cost,
        0,
        total_cost
    )
    
    time_stamp = get_current_time_stamp()
    file_name = "restock_RST-" + time_stamp + ".txt"
    if create_invoice_file(file_name, invoice_content):
        print("Restock invoice saved as " + file_name)
    return product_dict

def get_yes_no_input(prompt):
    """Gets yes/no input from user"""
    while True:
        response = input(prompt + "[y/n]: ").lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        print("Please enter 'y' or 'n'.")

def add_new_product(product_dict):
    """
    Adds a new product to inventory
    """
    print("\nEnter new product details:")
    product_name = input("Product name: ")
    product_brand = input("Brand: ")
    
    while True:
        try:
            product_quantity = int(input("Quantity: "))
            if product_quantity < 0:
                print("Quantity cannot be negative!")
                continue
            break
        except ValueError:
            print("Please enter a valid number!")
    
    while True:
        try:
            product_price = float(input("Price: "))
            if product_price <= 0:
                print("Price must be positive!")
                continue
            break
        except ValueError:
            print("Please enter a valid number!")
    
    product_origin = input("Origin: ")
    
    new_id = max(product_dict.keys(), default=0) + 1
    product_dict[new_id] = {
        'name': product_name,
        'brand': product_brand,
        'quantity': product_quantity,
        'price': product_price,
        'origin': product_origin
    }
    print("New product added with ID:", new_id)
    return product_dict
