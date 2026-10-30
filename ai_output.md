# AI-Generated Code Documentation — Lab 10

## AI Assistance

The original order lookup and chatbot were based on the instructor's provided examples. AI assistance was used to add the message-counting method, extend the chatbot with a stock lookup tool, and develop the banking FAQ mini-project.

The following sections contain the generated class code, including comments explaining the operations and their purpose.


## chatbot.py

```python
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
```

## stock_tool.py

```python
# stock_tool.py
# Author: Ananda Ravinder


class StockLookup:
    """A tool that checks product inventory without handling conversations."""

    def __init__(self, stock):
        """Store the product names and their available quantities."""
        self.stock = stock  # Keep inventory data on this tool object.

    def find_product(self, text):
        """Return a known product mentioned in the message, or None."""
        text = text.lower()  # Ignore capitalization when matching.
        for product in self.stock:  # Check each product in inventory.
            if product.lower() in text:  # Look for its name in the message.
                return product  # Return the matching product.
        return None  # No known product was mentioned.

    def count_for(self, product):
        """Return the available quantity, or None if not found."""
        if product in self.stock:  # Check whether the product exists.
            return self.stock[product]  # Return its available quantity.
        return None  # Product is unknown.
```

## my_tool.py

```python
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
```

## my_assistant.py

```python
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
```

## Code Explanations

### SupportChatbot

The original class came from the course lab. The AI-assisted changes added a stock lookup tool and a method for counting user messages.

- `__init__` stores the chatbot's name, instructions, order tool, stock tool, and an empty conversation history. Each attribute belongs to the current object.
- `respond` records the user message, selects a reply, records that reply, and returns it.
- `choose_reply` checks handoff requests first, followed by order questions, stock questions, and greetings. The order matters because sensitive requests should receive priority.
- `needs_human` checks each handoff keyword and returns a Boolean.
- `order_reply` uses the separate order tool to retrieve order information.
- `stock_reply` identifies a product using the stock tool, handles unknown products safely, and retrieves inventory quantities.
- `count_user_messages` loops through the conversation history and counts entries whose role is `user`.

### StockLookup

- `__init__` stores the inventory dictionary in `self.stock`.
- `find_product` converts the message to lowercase, loops through the known products, and returns the first matching product.
- `count_for` retrieves the quantity for a known product.
- Both lookup methods can return `None` when no match exists, allowing the chatbot to respond safely.
- Keeping inventory logic in its own class demonstrates composition.

### BankFAQTool

- `__init__` stores the FAQ dictionary as an object attribute.
- `find_topic` uses a loop to identify a known banking topic within the user's message.
- `get_answer` retrieves the answer for a recognized topic.
- Returning `None` for unknown topics prevents the assistant from inventing an answer.
- This class handles information retrieval rather than conversation management.

### BankingAssistant

- `HANDOFF_WORDS` defines the requests that require a bank representative.
- `__init__` stores the assistant's name and FAQ tool and initializes a separate history list.
- `respond` records the user's message and the assistant's reply.
- `choose_reply` checks sensitive requests first, handles greetings, routes questions to the FAQ tool, and returns a safe response for unsupported requests.
- `faq_reply` uses the FAQ tool to identify a topic and retrieve its answer. Failed lookups receive helpful responses instead of invented information.
- The assistant uses composition because it receives a `BankFAQTool` object rather than storing the FAQ lookup logic inside its own class.

## Verification

The original support chatbot, its extensions, and the banking mini-project were tested with Ruff and pytest. The completed project includes 17 passing tests.

