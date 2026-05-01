# data_handler.py
# [PROVIDED FILE - Do NOT modify]
# Description: File operations for Murphy's General Store Inventory System v4.0
#              Handles loading, saving, and exporting data.
#              ADAPTED FROM A3 to work with Product and Inventory objects.

"""
Data handler module.

This module provides functions for persistent storage and data export.
It handles loading and saving inventory and transactions as JSON,
and exporting reports as CSV and text files.

ADAPTED FROM A3: All functions updated to work with Product and Inventory objects.

YOU DO NOT NEED TO MODIFY THIS FILE - just include it in your submission.
"""

import json
import csv
from product import Product
from inventory import Inventory


# =============================================================================
# JSON PERSISTENCE FUNCTIONS (ADAPTED FROM A3)
# =============================================================================

def load_inventory(filename):
    """
    Load inventory from JSON file and create Inventory object with Product objects.
    
    Parameters:
        filename (str): Path to JSON file
    
    Returns:
        Inventory: Inventory object containing Product objects,
                   or empty Inventory if file not found or corrupted
    """
    inventory = Inventory()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert each product dict to Product object
        for product_id, product_data in data.items():
            product = Product.from_dict(product_id, product_data)
            inventory._products[product_id] = product
        
        print(f"Loaded {len(inventory)} products from {filename}")
        return inventory
        
    except FileNotFoundError:
        print(f"Note: {filename} not found. Starting with empty inventory.")
        return inventory
    
    except json.JSONDecodeError:
        print(f"Error: {filename} is corrupted. Starting with empty inventory.")
        return inventory
    
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return inventory


def save_inventory(inventory, filename):
    """
    Save inventory to JSON file.
    
    Parameters:
        inventory (Inventory): Inventory object to save
        filename (str): Path to JSON file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Convert all Product objects to dictionaries
        data = {}
        for product_id, product in inventory._products.items():
            data[product_id] = product.to_dict()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Inventory saved to {filename}")
        return True
        
    except Exception as e:
        print(f"Error saving inventory: {e}")
        return False


def load_transactions(filename):
    """
    Load transactions from JSON file.
    
    Parameters:
        filename (str): Path to JSON file
    
    Returns:
        list: List of transaction dictionaries,
              or empty list if file not found or corrupted
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            transactions = json.load(f)
        
        print(f"Loaded {len(transactions)} transactions from {filename}")
        return transactions
        
    except FileNotFoundError:
        print(f"Note: {filename} not found. Starting with empty transaction log.")
        return []
    
    except json.JSONDecodeError:
        print(f"Error: {filename} is corrupted. Starting with empty transaction log.")
        return []
    
    except Exception as e:
        print(f"Error loading transactions: {e}")
        return []


def save_transactions(transactions, filename):
    """
    Save transactions to JSON file.
    
    Parameters:
        transactions (list): List of transaction dictionaries
        filename (str): Path to JSON file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, indent=2, ensure_ascii=False)
        
        print(f"Transactions saved to {filename}")
        return True
        
    except Exception as e:
        print(f"Error saving transactions: {e}")
        return False


# =============================================================================
# EXPORT FUNCTIONS (ADAPTED FROM A3)
# =============================================================================

def export_inventory_to_csv(inventory, filename):
    """
    Export inventory to CSV file.
    
    Parameters:
        inventory (Inventory): Inventory object to export
        filename (str): Path to CSV file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['ID', 'Name', 'Category', 'Price', 'Quantity', 'Min Stock'])
            
            # Write each product
            for product in inventory.get_all_products():
                writer.writerow([
                    product.product_id,
                    product.name,
                    product.category,
                    f"{product.price:.2f}",
                    product.quantity,
                    product.min_stock
                ])
        
        print(f"Inventory exported to {filename}")
        return True
        
    except Exception as e:
        print(f"Error exporting inventory: {e}")
        return False


def export_low_stock_to_csv(inventory, filename):
    """
    Export low stock products to CSV file.
    
    Parameters:
        inventory (Inventory): Inventory object
        filename (str): Path to CSV file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        low_stock_products = inventory.get_low_stock_products()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['ID', 'Name', 'Category', 'Current', 'Minimum', 'Order'])
            
            # Write each low stock product
            for product in low_stock_products:
                order_qty = product.min_stock - product.quantity + 5
                writer.writerow([
                    product.product_id,
                    product.name,
                    product.category,
                    product.quantity,
                    product.min_stock,
                    order_qty
                ])
        
        print(f"Low stock report exported to {filename}")
        return True
        
    except Exception as e:
        print(f"Error exporting low stock report: {e}")
        return False


def generate_text_report(inventory, filename):
    """
    Generate formatted text report of inventory.
    
    Parameters:
        inventory (Inventory): Inventory object
        filename (str): Path to text file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write(" " * 15 + "MURPHY'S GENERAL STORE - INVENTORY REPORT\n")
            from datetime import datetime
            f.write(" " * 20 + f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Column headers
            f.write(f"{'ID':<8} {'Product':<20} {'Category':<15} {'Price':<10} "
                   f"{'Stock':<10} {'Min':<10}\n")
            f.write("=" * 80 + "\n")
            
            # Products
            for product in inventory.get_all_products():
                f.write(f"{product.product_id:<8} {product.name:<20} {product.category:<15} "
                       f"€{product.price:<9.2f} {product.quantity:<10} {product.min_stock:<10}\n")
            
            # Footer
            f.write("=" * 80 + "\n")
            total_value = inventory.calculate_total_value()
            f.write(f"Total Products: {len(inventory)}\n")
            f.write(f"Total Value: €{total_value:.2f}\n")
            f.write("=" * 80 + "\n")
        
        print(f"Report saved to {filename}")
        return True
        
    except Exception as e:
        print(f"Error generating report: {e}")
        return False
