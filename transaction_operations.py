# transaction_operations.py
# [PROVIDED FILE - Do NOT modify]
# Description: Transaction operations for Murphy's General Store Inventory System v4.0
#              Handles transaction logging and display.
#              REUSED FROM A2 - NO changes needed.

"""
Transaction operations module.

This module provides functions for logging and viewing transactions.
Transactions are stored as a simple list of dictionaries (same as A2/A3).

REUSED FROM A2: These functions are identical to A2 - no changes needed for A4.

YOU DO NOT NEED TO MODIFY THIS FILE - just include it in your submission.
"""

from datetime import datetime


def log_transaction(transactions, trans_type, product_id, product_name, quantity):
    """
    Log a transaction to the transaction list.
    
    REUSED FROM A2 - NO changes needed.
    
    Parameters:
        transactions (list): The transaction list
        trans_type (str): Type of transaction (e.g., "sale", "delivery", "added")
        product_id (str): Product ID
        product_name (str): Product name
        quantity (int): Quantity changed
    """
    transaction = {
        "type": trans_type,
        "product_id": product_id,
        "product_name": product_name,
        "quantity": quantity,
        "timestamp": datetime.now().isoformat()
    }
    transactions.append(transaction)


def view_transaction_log(transactions, num_recent=10):
    """
    Display recent transactions.
    
    REUSED FROM A2 - NO changes needed.
    
    Parameters:
        transactions (list): The transaction list
        num_recent (int): Number of recent transactions to display
    """
    if not transactions:
        print("No transactions recorded.")
        return
    
    # Get last N transactions in reverse order (most recent first)
    recent = list(reversed(transactions[-num_recent:]))
    
    print(f"\nShowing {len(recent)} most recent transaction(s):\n")
    
    for trans in recent:
        timestamp = datetime.fromisoformat(trans["timestamp"])
        date_str = timestamp.strftime('%Y-%m-%d %H:%M')
        qty_str = f"{trans['quantity']:+d}"  # Format with sign
        print(f"{date_str} - {trans['type'].upper()}: {trans['product_name']} "
              f"({trans['product_id']}), Qty: {qty_str}")
