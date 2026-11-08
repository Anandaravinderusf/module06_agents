# echo_model.py
# Author: Ananda Ravinder


class EchoModel:
    """A model that repeats the user's last message."""

    def reply(self, instructions, history):
        """Return the last message with a short prefix."""
        last_message = history[-1]["content"]  # Get the last message.
        return "You said: " + last_message  # Return the repeated message.
