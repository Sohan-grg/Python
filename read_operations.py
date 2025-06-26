def load_product_data():
    """
    Reads product data from products.txt and returns a dictionary of products
    """
    product_dict = {}
    try:
        data_file = open("products.txt", "r")
        product_id = 1
        for line in data_file:
            if count_commas(line) >= 4:
                parts = split_line(line, 4)
                product_dict[product_id] = {
                    'name': parts[0],
                    'brand': parts[1],
                    'quantity': convert_to_int(parts[2]),
                    'price': convert_to_float(parts[3]),
                    'origin': remove_newlines(parts[4])
                }
                product_id += 1
        data_file.close()
    except IOError:
        print("Product data file not found. Starting with empty inventory.")
    return product_dict

def count_commas(text):
    """Counts number of commas in a string"""
    count = 0
    for char in text:
        if char == ',':
            count += 1
    return count

def split_line(text, max_split):
    """Splits a line of text at commas"""
    parts = []
    current = ""
    split_count = 0
    for char in text:
        if char == ',' and split_count < max_split:
            parts.append(current)
            current = ""
            split_count += 1
        else:
            current += char
    parts.append(current)
    return parts

def convert_to_int(text):
    """Converts text to integer with error handling"""
    try:
        return int(text)
    except ValueError:
        return 0

def convert_to_float(text):
    """Converts text to float with error handling"""
    try:
        return float(text)
    except ValueError:
        return 0.0

def remove_newlines(text):
    """Removes newline characters from text"""
    clean_text = ""
    for char in text:
        if char not in ['\n', '\r']:
            clean_text += char
    return clean_text
