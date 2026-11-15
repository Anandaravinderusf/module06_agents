# fallback_model.py
# Author: Ananda Ravinder


class FallbackModel:
    """Use a backup model if the first model is unavailable."""

    def __init__(self, primary_model, fallback_model):
        """Store the two models."""
        self.primary_model = primary_model  # Try this model first.
        self.fallback_model = fallback_model  # Use this one if needed.

    def decide(self, instructions, history, tools):
        """Ask the primary model first, then the fallback if needed."""
        decision = self.primary_model.decide(
            instructions, history, tools
        )  # Get the primary model's decision.

        if decision is None:  # Check whether the primary model failed.
            return self.fallback_model.decide(
                instructions, history, tools
            )  # Ask the backup model instead.

        return decision  # Keep the primary model's successful decision.
