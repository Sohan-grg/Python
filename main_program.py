from read_operations import load_product_data
from write_operations import save_product_data
from business_operations import (
    display_product_inventory,
    process_product_sale,
    process_product_restock,
    add_new_product
)

def display_main_menu():
    """Displays the main menu options"""
    print("\n" + "=" * 50)
    print("WECARE WHOLESALE MANAGEMENT SYSTEM")
    print("=" * 50)
    print("\n1. Sell Products to Customer")
    print("2. Restock Products from Supplier")
    print("3. View Current Inventory")
    print("4. Add New Product to Inventory")
    print("5. Exit System")

def get_user_choice():
    """Gets and validates user menu choice"""
    while True:
        try:
            choice = int(input("\nEnter your choice (1-5): "))
            if 1 <= choice <= 5:
                return choice
            print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def main():
    """Main program function"""
    product_data = load_product_data()
    
    while True:
        display_main_menu()
        user_choice = get_user_choice()
        
        if user_choice == 1:
            updated_data = process_product_sale(product_data)
            if updated_data:
                product_data = updated_data
                save_product_data(product_data)
        elif user_choice == 2:
            updated_data = process_product_restock(product_data)
            if updated_data:
                product_data = updated_data
                save_product_data(product_data)
        elif user_choice == 3:
            display_product_inventory(product_data)
        elif user_choice == 4:
            updated_data = add_new_product(product_data)
            product_data = updated_data
            save_product_data(product_data)
        elif user_choice == 5:
            print("\nThank you for using WeCare Wholesale System. Goodbye!")
            break

if __name__ == "__main__":
    main()
