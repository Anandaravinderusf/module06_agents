# stock_tool.py
# Author: Ananda Ravinder


class StockLookup:
    """A tool that checks product inventory without handling conversations."""

    def __init__(self, stock):
        """Store the product names and their available quantities."""
        self.stock = stock

    def find_product(self, text):
        """Return a known product mentioned in the message, or None."""
        text = text.lower()
        for product in self.stock:
            if product.lower() in text:
                return product
        return None

    def count_for(self, product):
        """Return the available quantity, or None if not found."""
        if product in self.stock:
            return self.stock[product]
        return None

    def check_stock(self, item):
        """Check how many of one product are in stock.

        Args:
            item: The product name, like rain jacket.
        """
        product = self.find_product(item)
        if product is None:
            return "That product was not found."
        return f"We have {self.count_for(product)} of the {product} in stock."
