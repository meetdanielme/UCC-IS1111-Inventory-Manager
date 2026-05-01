# main.py
# Name: Daniel Marcinkowski
# Student ID: 125701129
# Date: 17/03/2026
# Description: Main programme module with menu system for inventory management using Product and Inventory classes.

"""
Main programme module for inventory management system.

This programme uses the Product and Inventory classes to manage Murphy's
General Store inventory with proper object-oriented design.
Transactions remain as a simple list (not a class).
"""

# =============================================================================
# IMPORTS
# =============================================================================
from datetime import datetime

# Import your classes
from product import Product
from inventory import Inventory

# Import modules
import data_handler
import transaction_operations
import inventory_operations


# =============================================================================
# INPUT VALIDATION FUNCTIONS (FROM A2)
# =============================================================================

def get_valid_float(prompt, min_value=0.0):
    """
    Prompt the user for a float value and validate it.
    
    REUSED FROM A2 - NO changes needed.
    
    Parameters:
        prompt (str): The message to display to the user
        min_value (float): The minimum acceptable value (default: 0.0)
    
    Returns:
        float: A valid float value >= min_value
    """
    while True:
        try:
            value = float(input(prompt))
            if value >= min_value:
                return value
            else:
                print(f"Error: Value must be at least {min_value}")
        except ValueError:
            print("Error: Please enter a valid number")


def get_valid_int(prompt, min_value=0):
    """
    Prompt the user for an integer value and validate it.
    
    REUSED FROM A2 - NO changes needed.
    
    Parameters:
        prompt (str): The message to display to the user
        min_value (int): The minimum acceptable value (default: 0)
    
    Returns:
        int: A valid integer value >= min_value
    """
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
            else:
                print(f"Error: Value must be at least {min_value}")
        except ValueError:
            print("Error: Please enter a valid whole number")


# =============================================================================
# MENU DISPLAY FUNCTIONS
# =============================================================================

def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("   Murphy's General Store - Inventory System")
    print("=" * 50)
    print("1. View All Products")
    print("2. Add New Product")
    print("3. Update Stock (Sale/Delivery)")
    print("4. Update Product Details")
    print("5. Remove Product")
    print("6. Search Products")
    print("7. View Low Stock Alerts")
    print("8. View Category Report")
    print("9. View Transaction Log")
    print("10. Export Reports")
    print("11. Save & Exit")
    print("=" * 50)


def handle_export_menu(inventory):
    """
    Handle the export reports submenu.
    
    Parameters:
        inventory (Inventory): The inventory object
    """
    while True:
        print("\n--- Export Reports ---")
        print("1. Export inventory to CSV")
        print("2. Export low stock report to CSV")
        print("3. Generate formatted text report")
        print("4. Export all reports")
        print("5. Cancel")
        
        choice = get_valid_int("Enter your choice (1-5): ", min_value=1)
        
        if choice == 5:
            break
        
        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
        if choice == 1:
            filename = f"inventory_{timestamp}.csv"
            data_handler.export_inventory_to_csv(inventory, filename)
        
        elif choice == 2:
            filename = f"low_stock_{timestamp}.csv"
            data_handler.export_low_stock_to_csv(inventory, filename)
        
        elif choice == 3:
            filename = f"inventory_report_{timestamp}.txt"
            data_handler.generate_text_report(inventory, filename)
        
        elif choice == 4:
            inv_file = f"inventory_{timestamp}.csv"
            low_file = f"low_stock_{timestamp}.csv"
            rep_file = f"inventory_report_{timestamp}.txt"
            
            data_handler.export_inventory_to_csv(inventory, inv_file)
            data_handler.export_low_stock_to_csv(inventory, low_file)
            data_handler.generate_text_report(inventory, rep_file)
            
            print("\nAll reports exported successfully!")
        
        else:
            print("Invalid choice. Please try again.")


# =============================================================================
# MAIN PROGRAMME
# =============================================================================

def main():
    """Main programme loop."""
    print("Welcome to Murphy's General Store Inventory System!")
    
    # Load data
    inventory = data_handler.load_inventory("inventory.json")
    transactions = data_handler.load_transactions("transactions.json")
    
    # Main menu loop
    while True:
        display_menu()
        choice = get_valid_int("Enter your choice (1-11): ", min_value=1)
        
        if choice == 1:
            inventory_operations.view_all_products_menu(inventory)
        
        elif choice == 2:
            inventory_operations.add_product_menu(inventory, transactions)
        
        elif choice == 3:
            inventory_operations.update_stock_menu(inventory, transactions)
        
        elif choice == 4:
            inventory_operations.update_product_details_menu(inventory)
        
        elif choice == 5:
            inventory_operations.remove_product_menu(inventory, transactions)
        
        elif choice == 6:
            inventory_operations.search_products_menu(inventory)
        
        elif choice == 7:
            inventory_operations.view_low_stock_menu(inventory)
        
        elif choice == 8:
            inventory_operations.view_category_report_menu(inventory)
        
        elif choice == 9:
            inventory_operations.view_transaction_log_menu(transactions)
        
        elif choice == 10:
            handle_export_menu(inventory)
        
        elif choice == 11:
            print("\nSaving data...")
            data_handler.save_inventory(inventory, "inventory.json")
            data_handler.save_transactions(transactions, "transactions.json")
            print("\nThank you for using Murphy's General Store Inventory System!")
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 11.")


if __name__ == "__main__":
    main()

# =============================================================================
# REFERENCES & AI STATEMENT
# =============================================================================
# References to any external sources used (following Canvas guidelines):
#
#
# AI Tool Usage:
# I acknowledge the use of GPT-5.3-Codex via GitHub Copilot
# (integrated into Visual Studio Code IDE) to generate inline
# code suggestions during development and to assist with code
# structure, formatting, and classes implementations.
# 
# The AI assistant provided suggestions for classes
# implementations, code structure, and formatting, which I
# reviewed, adapted, and integrated into my solution.
#
# The AI assistant provided autocomplete suggestions for:
# - Classes structure and formatting
# - Updating inventory_operations to use the Inventory class methods
#
# The AI assistant also helped me review my final code against
# the provided instructions, rubric, and checklists to ensure
# all requirements were met.
#
#
# =============================================================================

# =============================================================================
# SELF-REFLECTION (2-3 sentences)
# =============================================================================
# Write about the most challenging aspect of this assignment 
# and what you learned from it:
#
# Using classes instead of relaying on functions and dictionaries made a lot
# of sense for this kind of project and immidately made it obvious to me why
# one would want to use OOP and its principles. The implementation was straightforward. 
#
# =============================================================================