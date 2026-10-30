# chatbot.py
# Author: Ananda Ravinder

HANDOFF_WORDS = ["address", "payment", "card"]


class SupportChatbot:
    """A mock support chatbot using simple keyword rules."""

    def __init__(self, name, instructions, order_tool, stock_tool):
        """Set up the chatbot with its tools and conversation history."""
        self.name = name
        self.instructions = instructions
        self.order_tool = order_tool
        self.stock_tool = stock_tool  # Store the inventory tool for stock requests.
        self.history = []

    def respond(self, user_message):
        """Record the user message, generate a reply, and save both."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a reply based on keyword rules."""
        text = user_message.lower()

        if self.needs_human(text):
            return "I can't help with that here. I'm passing you to a human agent."

        if "order" in text:
            return self.order_reply(user_message)

        if "stock" in text:  # Identify inventory questions.
            return self.stock_reply(user_message)  # Ask the stock tool for an answer.

        if "hello" in text:
            return f"Hello! I'm {self.name}. I can check an order status for you."

        return "I'm not sure how to help with that. I can check an order status."

    def needs_human(self, text):
        """Return True for requests requiring human approval."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def order_reply(self, user_message):
        """Use the order tool to answer an order question."""
        order_id = self.order_tool.find_order_id(user_message)
        if order_id is None:
            return "Which order? Please send an order ID like A100."
        status = self.order_tool.find_status(order_id)
        return f"Order {order_id} is {status}."

    def stock_reply(self, user_message):
        """Use the stock tool to answer an inventory question."""
        product = self.stock_tool.find_product(user_message)  # Identify the item.
        if product is None:  # Ask for clarification if no item matches.
            return "Which product? Please name the item you want me to check."
        count = self.stock_tool.count_for(product)  # Look up available quantity.
        return f"We have {count} of the {product} in stock."

    def count_user_messages(self):
        """Return the number of user messages in the conversation."""
        count = 0
        for message in self.history:
            if message["role"] == "user":
                count += 1
        return count
