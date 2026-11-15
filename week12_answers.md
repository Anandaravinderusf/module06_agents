
# Week 12 Answers

## Exercise 1

1. The customer typed three messages:
   - I want to change my shipping address
   - It's order A102
   - 9 Pine Street, Tampa

2. Two tool requests were refused. The first used an order ID the customer had not provided, and the second used a shipping address the customer had not provided.

3. If the customer types "thanks", Ollama receives 14 messages. This includes the system instructions, the new user message, and the conversation history. Each tool entry is converted into two messages for Ollama.

4. The gift card question goes to a person because "card" is one of the handoff keywords in the chatbot's code. This is acceptable because the chatbot is being cautious and sends the request to a human instead of potentially giving incorrect information.


## Exercise 3

I temporarily disabled the customer_said check in toolbox.py and asked the chatbot to change my shipping address.

You: I want to change my shipping address
Sunny: Could you please provide the order ID for the order you'd like to change the shipping address on?
You: quit
Messages in this conversation: 3

Staff review
A100 14 Bay Road
A101 3 Gull Lane
A102 88 Pier Street

In my test, the chatbot asked for the order ID instead of creating an address-change request. No change was waiting for approval, and the addresses stayed the same. Even though the model did not visibly invent details in this run, disabling the guardrail is risky because the toolbox would no longer verify that the customer actually provided the requested information. I restored the guardrail afterward and all 39 tests passed.

## Exercise 4

I created FallbackModel to try Ollama first and use KeywordModel if Ollama is unavailable. I tested it by connecting to a local port where Ollama was not running.

You: hello
Sunny: Hello! How can I help you today.
You: Where is order A100?
Sunny: Order A100 is shipped.
You: quit
Messages in this conversation: 5

The fallback allowed the chatbot to answer a greeting and look up an order even though the primary model was unavailable. The order lookup still used the toolbox, so its checks stayed in place.
