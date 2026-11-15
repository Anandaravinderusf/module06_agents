# my_tool.py
# Author: Ananda Ravinder


class BankFAQTool:
    """Look up answers to common banking questions."""

    def __init__(self, faqs):
        """Store the available FAQ topics and answers."""
        self.faqs = faqs

    def find_topic(self, text):
        """Find a known FAQ topic mentioned in a message."""
        text = text.lower()
        for topic in self.faqs:
            if topic in text:
                return topic
        return None

    def get_answer(self, topic):
        """Return an FAQ answer, or None if the topic is unknown."""
        if topic in self.faqs:
            return self.faqs[topic]
        return None

    def look_up_faq(self, topic):
        """Look up information about a banking topic.

        Args:
            topic: The banking topic, like business loans.
        """
        found = self.find_topic(topic)
        if found is None:
            return "I don't have information about that banking topic."
        return self.get_answer(found)
