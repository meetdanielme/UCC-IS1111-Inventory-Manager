# product.py
# Name: Daniel Marcinkowski
# Student ID: 125701129
# Date: 17/03/2026
# Description: Product class for inventory management with price and stock validation.

"""
Product module for Murphy's General Store inventory system.

Defines the Product class with encapsulation, validation, and serialisation helpers.
"""

class Product:

    def __init__(self, product_id, name, category, price, quantity, min_stock):
        """The Product class represents a single product with validation.
        
        Attributes:
         - product_id (str) - Unique identifier, read-only
        - name (str) - Product name, validated
        - category (str) - Product category, validated
        - price (float) - Price per unit, must be >= 0
        - quantity (int) - Current stock quantity, must be >= 0
        - min_stock (int) - Minimum stock level, must be >= 0
        """
        self.__product_id = product_id  # read-only, no setter, so assigned directly
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.min_stock = min_stock

    # ==== getters & setters ====

    # === product_id ===
    @property
    def product_id(self):
        """
        The product_id is a unique identifier for the product and is read-only.
        
        Returns:
            str: The unique product ID."""
        return self.__product_id
    
    # === name ===
    @property
    def name(self):
        """
        The name of the product. Must be a non-empty string.
        
        Returns:
            str: The name of the product."""
        return self.__name
    
    @name.setter
    def name(self, new_name):
        """
        Set the name of the product. Must be a non-empty string.
        
        Parameters:
            new_name (str): The new name for the product.
            
        Raises:
            ValueError: If new_name is empty or only whitespace.
        """
        if new_name.strip() == "":
            raise ValueError("Product name cannot be empty.")
        self.__name = new_name

    # === category ===
    @property
    def category(self):
        """
        The category of the product. Must be a non-empty string.

        Returns:
            str: The category of the product.
        """
        return self.__category
    
    @category.setter
    def category(self, new_category):
        """
        Set the category of the product. Must be a non-empty string.

        Parameters:
            new_category (str): The new category for the product.

        Raises:
            ValueError: If new_category is empty or only whitespace.
        """
        if new_category.strip() == "":
            raise ValueError("Product category cannot be empty.")
        self.__category = new_category

    # === price ===
    @property
    def price(self):
        """
        The price per unit of the product. Must be >= 0.

        Returns:
            float: The price per unit.
        """
        return self.__price
    
    @price.setter
    def price(self, new_price):
        """
        Set the price per unit. Must be >= 0.

        Parameters:
            new_price (float): The new price per unit.

        Raises:
            ValueError: If new_price is negative.
        """
        if new_price < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = new_price

    # === quantity ===
    @property
    def quantity(self):
        """
        The current stock quantity of the product. Must be >= 0.

        Returns:
            int: The current stock quantity.
        """
        return self.__quantity

    @quantity.setter
    def quantity(self, new_quantity):
        """
        Set the current stock quantity. Must be >= 0.

        Parameters:
            new_quantity (int): The new stock quantity.

        Raises:
            ValueError: If new_quantity is negative.
        """
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.__quantity = new_quantity

    # === min_stock ===
    @property
    def min_stock(self):
        """
        The minimum stock level before a low stock alert is triggered. Must be >= 0.

        Returns:
            int: The minimum stock level.
        """
        return self.__min_stock
    
    @min_stock.setter
    def min_stock(self, new_min_stock):
        """
        Set the minimum stock level. Must be >= 0.

        Parameters:
            new_min_stock (int): The new minimum stock level.

        Raises:
            ValueError: If new_min_stock is negative.
        """
        if new_min_stock < 0:
            raise ValueError("Minimum stock cannot be negative.")
        self.__min_stock = new_min_stock

    # ==== other methods ====

    def update_stock(self, amount_change):
        """
        Add or remove stock from the product.

        Parameters:
            amount_change (int): Amount to add (positive) or remove (negative).

        Raises:
            ValueError: If the resulting quantity would be negative.
        """
        if self.__quantity + amount_change < 0:
            raise ValueError("Cannot reduce stock below zero.")
        self.__quantity += amount_change

    def get_value(self):
        """
        Calculate the total stock value of this product (price × quantity).

        Returns:
            float: Total value of the product.
        """
        return self.__price * self.__quantity
    
    def is_low_stock(self):
        """
        Check whether the product needs reordering.

        Returns:
            bool: True if quantity is below min_stock, False otherwise.
        """
        return self.__quantity < self.__min_stock
    
    def to_dict(self):
        """
        Convert the product to a dictionary for JSON storage.
        Note: product_id is excluded as it is used as the dictionary key.

        Returns:
            dict: Product data with keys: name, category, price, quantity, min_stock.
        """
        return {
            "name": self.__name,
            "category": self.__category,
            "price": self.__price,
            "quantity": self.__quantity,
            "min_stock": self.__min_stock
        }
    
    @classmethod
    def from_dict(cls, product_id, data):
        """
        Create a Product object from a dictionary (e.g. loaded from JSON).

        Parameters:
            product_id (str): The unique product ID (stored as the JSON key).
            data (dict): Dictionary containing product data.

        Returns:
            Product: A new Product object.
        """
        product = cls(
            product_id=product_id,
            name=data.get("name", ""),
            category=data.get("category", ""),
            price=data.get("price", 0),
            quantity=data.get("quantity", 0),
            min_stock=data.get("min_stock", 0)
        )
        return product
    
    def __str__(self):
        """
        Return a readable string representation of the product.

        Returns:
            str: Formatted string including ID, name, category, price, quantity, and min stock.
        """
        return f"Product ID: {self.__product_id}, Name: {self.__name}, Category: {self.__category}, Price: {self.__price}, Quantity: {self.__quantity}, Min Stock: {self.__min_stock}"