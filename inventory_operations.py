# inventory_operations.py
# Name: Daniel Marcinkowski
# Student ID: 125701129
# Date: 17/03/2026
# Description: Menu handler functions for inventory management operations including add, search, update, and reporting.

"""
Inventory operations module.

This module contains all menu handler functions for inventory management.
These functions interact with Product and Inventory objects.

ADAPTED FROM A3: Replace TODO sections to use class methods instead of 
dictionary operations.
"""

import transaction_operations


# =============================================================================
# MENU HANDLER FUNCTIONS (ADAPT FROM A3)
# =============================================================================
# These functions are based on the A3 code.
# UPDATE the marked TODO sections to use Product and Inventory class methods.

def view_all_products_menu(inventory):
    """Display all products in formatted table."""
    print("\n--- All Products ---")
    
    products = inventory.get_all_products()
    
    if not products:
        print("No products in inventory.")
        return
    
    print(f"{'ID':<6} {'Product':<20} {'Category':<15} {'Price':<10} {'Stock':<10} {'Min Stock':<10}")
    print("=" * 71)
    
    for product in products:
        print(f"{product.product_id:<6} {product.name:<20} {product.category:<15} €{product.price:<9.2f} {product.quantity:<10} {product.min_stock:<10}")
    
    print("=" * 71)
    print(f"Total products: {len(inventory)}")


def add_product_menu(inventory, transactions):
    """Add a new product to inventory."""
    print("\n--- Add New Product ---")
    
    # Get product name (REUSABLE - no changes needed)
    name = input("Enter product name: ").strip()
    
    existing_id = inventory.find_by_name(name)
    if existing_id is not None:
        print(f"Error: A product with the name '{name}' already exists (ID: {existing_id}). Please choose a different name.")
        return None

    # Get remaining details (REUSABLE - no changes needed)
    from main import get_valid_float, get_valid_int
    category = input("Enter category: ").strip()
    price = get_valid_float("Enter price (€): ", min_value=0.01)
    qty = get_valid_int("Enter current stock quantity: ", min_value=0)
    min_stock = get_valid_int("Enter minimum stock level: ", min_value=0)
    
    product_id = inventory.add_product(name, category, price, qty, min_stock)
    
    # Log transaction (REUSABLE - no changes needed)
    transaction_operations.log_transaction(transactions, "added", product_id, name, qty)
    
    print(f"\nProduct '{name}' added successfully with ID: {product_id}")
    return product_id


def update_stock_menu(inventory, transactions):
    """Update stock for a product (sale or delivery)."""
    print("\n--- Update Stock ---")
    
    name = input("Enter product name: ").strip()
    product_id = inventory.find_by_name(name)
    
    if product_id is None:
        print(f"Error: Product '{name}' not found in inventory.")
        return False
    
    product = inventory.get_product(product_id)
    
    transaction_type = input("Is this a (S)ale or (D)elivery? ").strip().lower()
    
    while transaction_type not in ['s', 'd', 'sale', 'delivery']:
        print("Error: Please enter 'S' for sale or 'D' for delivery")
        transaction_type = input("Is this a (S)ale or (D)elivery? ").strip().lower()
    
    from main import get_valid_int
    quantity = get_valid_int("Enter quantity: ", min_value=1)
    
    try:
        if transaction_type in ['s', 'sale']:
            product.update_stock(-quantity)
            trans_type = "sale"
            change = -quantity
        else:
            product.update_stock(quantity)
            trans_type = "delivery"
            change = quantity
        
        transaction_operations.log_transaction(transactions, trans_type, product_id, product.name, change)
        print(f"\nStock updated! {product.name} now has {product.quantity} units.")
        return True
        
    except ValueError as e:
        print(f"Error: {e}")
        return False


def update_product_details_menu(inventory):
    """Update product details (name, category, price, min_stock)."""
    print("\n--- Update Product Details ---")
    
    name = input("Enter product name: ").strip()
    product_id = inventory.find_by_name(name)
    
    if product_id is None:
        print(f"Error: Product '{name}' not found in inventory.")
        return False
    
    product = inventory.get_product(product_id)
    
    print(f"\nCurrent details for {product.name}:")
    print(f"  Name: {product.name}")
    print(f"  Category: {product.category}")
    print(f"  Price: €{product.price:.2f}")
    print(f"  Min Stock: {product.min_stock}")
    
    # Get update choice (REUSABLE - no changes needed)
    print("\nWhat would you like to update?")
    print("1. Name")
    print("2. Category")
    print("3. Price")
    print("4. Minimum Stock Level")
    print("5. Cancel")
    
    from main import get_valid_int
    choice = get_valid_int("Enter your choice (1-5): ", min_value=1)
    
    while choice not in range(1, 6):
        print("Error: Please enter a number between 1 and 5")
        choice = get_valid_int("Enter your choice (1-5): ", min_value=1)
    
    if choice == 5:
        print("Update cancelled.")
        return False
    
    try:
        if choice == 1:
            new_name = input("Enter new name: ").strip()
            product.name = new_name
            print(f"\nName updated successfully to: {new_name}")
        
        elif choice == 2:
            new_category = input("Enter new category: ").strip()
            product.category = new_category
            print(f"\nCategory updated successfully to: {new_category}")
        
        elif choice == 3:
            from main import get_valid_float
            new_price = get_valid_float("Enter new price (€): ", min_value=0.01)
            product.price = new_price
            print(f"\nPrice updated successfully to: €{new_price:.2f}")
        
        elif choice == 4:
            new_min_stock = get_valid_int("Enter new minimum stock level: ", min_value=0)
            product.min_stock = new_min_stock
            print(f"\nMinimum stock level updated successfully to: {new_min_stock}")
        
        return True
        
    except ValueError as e:
        print(f"Error: {e}")
        return False


def remove_product_menu(inventory, transactions):
    """Remove a product from inventory."""
    print("\n--- Remove Product ---")
    
    name = input("Enter product name to remove: ").strip()
    product_id = inventory.find_by_name(name)
    
    if product_id is None:
        print(f"Error: Product '{name}' not found in inventory.")
        return False
    
    confirm = input(f"Are you sure you want to remove '{name}'? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        removed = inventory.remove_product(product_id)
        
        if removed:
            transaction_operations.log_transaction(transactions, "removed", product_id, removed.name, 0)
            print(f"\nProduct '{removed.name}' removed successfully.")
            return True
    else:
        print("Removal cancelled.")
        return False


def search_products_menu(inventory):
    """Search for products by name or category."""
    print("\n--- Search Products ---")
    print("1. Search by name")
    print("2. Search by category")
    
    from main import get_valid_int
    choice = get_valid_int("Enter your choice (1-2): ", min_value=1)
    
    while choice not in [1, 2]:
        print("Error: Please enter 1 or 2")
        choice = get_valid_int("Enter your choice (1-2): ", min_value=1)
    
    if choice == 1:
        search_term = input("Enter product name (or part of name): ").strip()
        results = inventory.search_by_name(search_term)
    else:
        category = input("Enter category: ").strip()
        results = inventory.search_by_category(category)
    
    if not results:
        print("No products found matching your search.")
        return
    
    print(f"\nFound {len(results)} product(s):\n")
    print(f"{'ID':<6} {'Product':<20} {'Category':<15} {'Price':<10} {'Stock':<10}")
    print("=" * 61)
    
    for product in results:
        print(f"{product.product_id:<6} {product.name:<20} {product.category:<15} €{product.price:<9.2f} {product.quantity:<10}")


def view_low_stock_menu(inventory):
    """Display products at or below minimum stock levels."""
    print("\n--- Low Stock Alerts ---")
    
    low_stock = inventory.get_low_stock_products()
    
    if not low_stock:
        print("No products are currently low on stock.")
        return
    
    print(f"Found {len(low_stock)} product(s) needing restocking:\n")
    print(f"{'ID':<6} {'Product':<20} {'Category':<15} {'Current':<10} {'Minimum':<10}")
    print("=" * 61)
    
    for product in low_stock:
        print(f"{product.product_id:<6} {product.name:<20} {product.category:<15} {product.quantity:<10} {product.min_stock:<10}")


def view_category_report_menu(inventory):
    """Generate and display category report."""
    print("\n--- Category Report ---")
    
    report = inventory.generate_category_report()
    
    if not report:
        print("No products in inventory.")
        return
    
    print(f"{'Category':<20} {'Count':<10} {'Total Value':<15}")
    print("=" * 45)
    
    total_products = 0
    total_value = 0.0
    
    for category, stats in sorted(report.items()):
        count = stats["count"]
        value = stats["total_value"]
        print(f"{category:<20} {count:<10} €{value:<14.2f}")
        total_products += count
        total_value += value
    
    print("=" * 45)
    print(f"{'TOTAL':<20} {total_products:<10} €{total_value:<14.2f}")


def view_transaction_log_menu(transactions):
    """View recent transaction history."""
    print("\n--- Transaction Log ---")
    
    if not transactions:
        print("No transactions recorded.")
        return
    
    from main import get_valid_int
    num = get_valid_int("How many recent transactions to display? (default 10): ", min_value=1)
    
    # Use transaction_operations module (REUSABLE - no changes needed)
    transaction_operations.view_transaction_log(transactions, num)
