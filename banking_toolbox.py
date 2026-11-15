# banking_toolbox.py
# Author: Ananda Ravinder


class BankingToolbox:
    """Check every tool request before allowing it to run."""

    def __init__(self, faq_tool, contact_queue):
        """Store the FAQ tool and the contact change queue."""
        self.faq_tool = faq_tool
        self.contact_queue = contact_queue

    def tool_list(self):
        """Return the tools available to the banking assistant."""
        return [
            self.faq_tool.look_up_faq,
            self.contact_queue.request_contact_change,
        ]

    def run(self, name, arguments, history):
        """Check the arguments before running a requested tool."""
        if name == "look_up_faq":
            topic = self.clean(arguments, "topic")

            if topic == "":
                return "The banking topic is missing. Ask the customer."

            if not self.customer_said(history, topic):
                return "The customer has not mentioned that banking topic."

            return self.faq_tool.look_up_faq(topic)

        if name == "request_contact_change":
            customer_id = self.clean(arguments, "customer_id")
            new_method = self.clean(arguments, "new_method")

            if customer_id == "" or new_method == "":
                return "The customer ID and contact method are both needed."

            if not self.customer_said(history, customer_id):
                return "The customer has not provided that customer ID."

            if not self.customer_said(history, new_method):
                return "The customer has not requested that contact method."

            return self.contact_queue.request_contact_change(customer_id, new_method)

        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text with extra spaces removed."""
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        """Check whether the customer actually provided the information."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
