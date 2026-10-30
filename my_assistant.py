# my_assistant.py
# Author: Ananda Ravinder

HANDOFF_WORDS = ["change my", "transfer money", "send money", "approve my"]


class BankingAssistant:
    """A mock banking FAQ assistant with a separate lookup tool."""

    def __init__(self, name, faq_tool):
        """Give each assistant a name, a tool, and its own history."""
        self.name = name  # Store this assistant's name.
        self.faq_tool = faq_tool  # Store the FAQ lookup tool.
        self.history = []  # Start a separate conversation history.

    def respond(self, user_message):
        """Record a user message and the assistant's reply."""
        self.history.append(
            {"role": "user", "content": user_message}
        )  # Save the user's message.

        reply = self.choose_reply(user_message)  # Select a response.

        self.history.append(
            {"role": "assistant", "content": reply}
        )  # Save the assistant's reply.

        return reply  # Return the response to the caller.

    def choose_reply(self, user_message):
        """Choose between a handoff, FAQ lookup, or safe reply."""
        text = user_message.lower()  # Normalize the message.

        for word in HANDOFF_WORDS:  # Check requests needing approval.
            if word in text:  # Identify a sensitive action.
                return (
                    "I can't make that change. I'll refer you to a bank representative."
                )

        if "hello" in text:  # Handle a greeting.
            return f"Hello! I'm {self.name}. I can answer common banking questions."

        if "?" in text or "tell me" in text:  # Recognize a question.
            return self.faq_reply(user_message)  # Use the separate FAQ tool.

        return "I'm not sure how to help with that. I can answer banking FAQs."

    def faq_reply(self, user_message):
        """Use the FAQ tool without inventing an answer."""
        topic = self.faq_tool.find_topic(user_message)  # Find a matching topic.

        if topic is None:  # Handle an unsuccessful lookup.
            return "I don't have that information. Ask about business loans, savings accounts, or wire transfers."

        answer = self.faq_tool.get_answer(topic)  # Retrieve the stored answer.

        if answer is None:  # Handle missing information safely.
            return "I couldn't find an answer for that topic."

        return answer  # Return the verified mock FAQ answer.
