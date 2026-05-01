# inventory.py
# Name: Daniel Marcinkowski
# Student ID: 125701129
# Date: 17/03/2026
# Description: Inventory class for managing a collection of Product objects with search and reporting capabilities.

"""
Inventory module for Murphy's General Store inventory system.

Defines the Inventory class that manages Product objects and reporting utilities.
"""

from product import Product


class Inventory:
    """Manage a collection of Product objects keyed by product ID."""

    # ==== constructor ====
    def __init__(self):
        """
        Initialise an empty inventory.

        The internal dictionary maps product IDs (str) to Product objects.
        """
        self._products = {}

    # ==== methods ====
    def add_product(self, name, category, price, quantity, min_stock):
        """
        Add a new product to the inventory.

        A unique product ID is generated automatically, then a Product
        object is created and stored in _products.

        Parameters:
            name (str): The name of the product.
            category (str): The category of the product.
            price (float): Price per unit.
            quantity (int): Current stock quantity.
            min_stock (int): Minimum stock level.

        Returns:
            str: The new product ID.
        """
        new_product_id = self._generate_id()
        new_product = Product(new_product_id, name, category, price, quantity, min_stock)
        self._products[new_product_id] = new_product
        return new_product_id

    def remove_product(self, product_id):
        """
        Remove a product from the inventory by product ID.

        Parameters:
            product_id (str): The product ID to remove.

        Returns:
            Product | None: The removed Product object, or None if not found.
        """

        if product_id in self._products:
            product = self._products[product_id]  # save reference before deleting
            del self._products[product_id]
            return product
        return None

    def get_product(self, product_id):
        """
        Get a single product by product ID.

        Parameters:
            product_id (str): The product ID to look up.

        Returns:
            Product | None: Matching Product object, or None if not found.
        """
        return self._products.get(product_id)   
    
    def get_all_products(self):
        """Return a list of all Product objects in the inventory."""
        return list(self._products.values())
    
    def find_by_name(self, name):
        """
        Find a product ID by exact name match (case-insensitive).

        Parameters:
            name (str): Product name to match.

        Returns:
            str | None: Matching product ID, or None if not found.
        """
        for product_id, product in self._products.items():
            if product.name.lower() == name.lower():
                return product_id
        return None
    
    def search_by_name(self, search_term):
        """
        Search products by partial name match (case-insensitive).

        Parameters:
            search_term (str): Text to search for in product names.

        Returns:
            list[Product]: Matching Product objects.
        """
        return [p for p in self._products.values() if search_term.lower() in p.name.lower()] # Case-insensitive partial match
    
    def search_by_category(self, category):
        """
        Search products by exact category match (case-insensitive).

        Parameters:
            category (str): Category to match.

        Returns:
            list[Product]: Matching Product objects.
        """
        return [p for p in self._products.values() if p.category.lower() == category.lower()] # Case-insensitive exact category match
    
    def get_low_stock_products(self):
        """
        Get all products that are below their minimum stock level.

        Returns:
            list[Product]: Products where quantity is below min_stock.
        """
        return [p for p in self._products.values() if p.quantity < p.min_stock]
    
    def generate_category_report(self):
        """
        Generate category statistics for the inventory.

        Returns:
            dict: For each category, includes product count and total value.
        """
        report = {}
        for product in self._products.values():
            cat = product.category
            if cat not in report:
                report[cat] = {"count": 0, "total_value": 0.0}
            report[cat]["count"] += 1
            report[cat]["total_value"] += product.get_value()
        return report
    
    def calculate_total_value(self):
        """
        Calculate the total monetary value of all products in inventory.

        Returns:
            float: Sum of (price * quantity) across all products.
        """
        return sum(p.get_value() for p in self._products.values())

    def _generate_id(self):
        """
        Generate the next unique product ID.

        Returns:
            str: Product ID in the format P### (for example, P001).
        """
        if not self._products:
            return "P001"
        highest = max(int(pid[1:]) for pid in self._products)
        return f"P{highest + 1:03d}" 
    
    def __len__(self):
        """
        Return the number of products in the inventory.

        Returns:
            int: Count of products.
        """
        return len(self._products)