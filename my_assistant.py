# my_assistant.py
# Author: Ananda Ravinder

HANDOFF_WORDS = ["change my", "transfer money", "send money", "approve my"]


class BankingAssistant:
    """A banking FAQ assistant that uses a lookup tool and a model."""

    def __init__(self, name, instructions, faq_tool, model):
        """Store the assistant's settings, tools, and conversation history."""
        self.name = name  # Store the assistant's name.
        self.instructions = instructions  # Store instructions for the model.
        self.faq_tool = faq_tool  # Store the banking FAQ lookup tool.
        self.model = model  # Store the model used for other questions.
        self.history = []  # Keep a separate conversation history.

    def respond(self, user_message):
        """Save the user's message and the assistant's response."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Check banking rules first, then use the model."""
        text = user_message.lower()

        for word in HANDOFF_WORDS:
            if word in text:
                return (
                    "I can't make that change. I'll refer you to a bank representative."
                )

        topic = self.faq_tool.find_topic(user_message)
        if topic is not None:
            return self.faq_reply(user_message)

        return self.model_reply()

    def faq_reply(self, user_message):
        """Use the FAQ tool to answer supported banking questions."""
        topic = self.faq_tool.find_topic(user_message)

        if topic is None:
            return "I couldn't find a matching banking topic."

        answer = self.faq_tool.get_answer(topic)
        if answer is None:
            return "I couldn't find an answer for that topic."

        return answer

    def model_reply(self):
        """Ask the model for a reply, or give a safe fallback."""
        reply = self.model.reply(self.instructions, self.history)

        if reply is None:
            return "Sorry, I can't answer that right now. Please contact a bank representative."

        return reply
