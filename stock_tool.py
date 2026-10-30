# stock_tool.py
# Author: Ananda Ravinder


class StockLookup:
    """A tool that checks product inventory without handling conversations."""

    def __init__(self, stock):
        """Store the product names and their available quantities."""
        self.stock = stock  # Keep inventory data on this tool object.

    def find_product(self, text):
        """Return a known product mentioned in the message, or None."""
        text = text.lower()  # Ignore capitalization when matching.
        for product in self.stock:  # Check each product in inventory.
            if product.lower() in text:  # Look for its name in the message.
                return product  # Return the matching product.
        return None  # No known product was mentioned.

    def count_for(self, product):
        """Return the available quantity, or None if not found."""
        if product in self.stock:  # Check whether the product exists.
            return self.stock[product]  # Return its available quantity.
        return None  # Product is unknown.
