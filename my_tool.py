# my_tool.py
# Author: Ananda Ravinder


class BankFAQTool:
    """Look up answers to common banking questions."""

    def __init__(self, faqs):
        """Store the available FAQ topics and answers."""
        self.faqs = faqs  # Keep the FAQ dictionary on this tool object.

    def find_topic(self, text):
        """Find a known FAQ topic mentioned in a message."""
        text = text.lower()  # Make matching case-insensitive.

        for topic in self.faqs:  # Check every available topic.
            if topic in text:  # Look for the topic in the message.
                return topic  # Return the first matching topic.

        return None  # No FAQ topic matched the message.

    def get_answer(self, topic):
        """Return an FAQ answer, or None if the topic is unknown."""
        if topic in self.faqs:  # Check that the topic exists.
            return self.faqs[topic]  # Return the stored answer.

        return None  # Do not invent an answer for unknown topics.
