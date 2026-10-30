
# ISM3232 Lab 10 — OOP for Agents

**Author:** Ananda Ravinder  
**Course:** ISM3232 - Business Application Development

## Project Overview

This lab demonstrates object-oriented programming by building a support chatbot and separate lookup tools. The chatbot can answer order-status questions, check product inventory, and keep a conversation history. It also demonstrates composition by allowing multiple chatbot objects to share tools while maintaining separate histories.

## Mini-Project: Banking FAQ Assistant

My mini-project is a banking FAQ assistant named Finley that answers common questions about business loans, savings accounts, and wire transfers. The assistant uses a separate FAQ lookup class to find answers and keeps a history of user messages and responses. It is a mock system because the answers come from a small dictionary instead of a real bank database or AI model. Requests involving account changes or money transfers are referred to a bank representative because those actions require authorization. If the assistant used real customer data, a potential risk would be exposing sensitive financial information through its conversation history. Unknown questions receive a safe response instead of a made-up answer.

## How to Run

Activate the virtual environment and install the project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the original support chatbot:

```bash
python3 main.py
```

Run the two-chatbot demonstration:

```bash
python3 two_bots.py
```

Run the banking assistant:

```bash
python3 my_main.py
```

Type `quit` to end either interactive conversation.

## How to Test

```bash
ruff format .
ruff check .
pytest -v
```

The project includes 17 passing tests: 10 for the support chatbot and its tools, and 7 for the banking assistant.

## Project Files

- `order_tool.py` — Order-status lookup class.
- `chatbot.py` — Support chatbot with order and inventory tools.
- `stock_tool.py` — Product inventory lookup class.
- `main.py` — Interactive support chatbot.
- `two_bots.py` — Demonstrates two independent chatbot objects.
- `exercise1.md` — Identifies classes, objects, attributes, methods, and composition.
- `my_tool.py` — Banking FAQ lookup tool.
- `my_assistant.py` — Banking FAQ assistant class.
- `my_main.py` — Interactive banking assistant.
- `tests/test_chatbot.py` — Support chatbot tests.
- `tests/test_my_assistant.py` — Banking assistant tests.
- `ai_output.md` — Documents AI-generated class code and explanations.
- `requirements.txt` — Project dependencies.
- `.gitignore` — Excludes virtual environments and cache files.

## AI Use Documentation
I followed the course examples to build the original support chatbot and order lookup tool. I used AI assistance for some of the class extensions and the banking assistant mini-project. The AI-generated class code and explanations are documented in `ai_output.md`. I ran the programs, checked their outputs, and verified all 17 tests using pytest and Ruff.
