# my_assistant.py
# Author: Ananda Ravinder

HANDOFF_WORDS = [
    "change my account",
    "transfer money",
    "send money",
    "approve my",
]

MAX_TOOL_ROUNDS = 3


class BankingAssistant:
    """A banking assistant that uses tools and checks requests before running them."""

    def __init__(self, name, instructions, tools, model):
        """Store the assistant's information, toolbox, model, and history."""
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user's message and the assistant's response."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Handle sensitive requests first, then ask the model."""
        text = user_message.lower()

        for word in HANDOFF_WORDS:
            if word in text:
                return (
                    "I can't make that change. I'll refer you to a bank representative."
                )

        return self.model_reply()

    def model_reply(self):
        """Let the model choose tools, with a limit on tool requests."""
        rounds = 0

        while rounds < MAX_TOOL_ROUNDS:
            tool_list = self.tools.tool_list()
            decision = self.model.decide(self.instructions, self.history, tool_list)

            if decision is None:
                return "Sorry, I can't answer that right now. Please contact a bank representative."

            if "text" in decision:
                return decision["text"]

            name = decision["tool"]
            arguments = decision["arguments"]

            result = self.tools.run(name, arguments, self.history)

            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )

            rounds += 1

        return "Sorry, I couldn't finish that request. Please contact a bank representative."
