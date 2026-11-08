
# ISM3232 — OOP for Agents and Local Models

**Author:** Ananda Ravinder  
**Course:** ISM3232 - Business Application Development

## Project Overview

This project builds on the Week 10 support chatbot by adding a local AI model through Ollama. The chatbot uses Python rules and separate tools to handle order statuses, inventory questions, and requests that need a human agent. Other messages are sent to the local model. The project also demonstrates conversation history, composition, and how to handle situations when the model is unavailable.

## Week 11 — Local Model

I used Ollama with the `granite4.1:3b` model to test how an AI assistant responds to instructions and conversation history. In the first experiment, the model gave different store hours because none were provided in the instructions. I also tested two separate conversations to see how sending previous messages affects the model's ability to remember information. The chatbot now uses a mock model for testing and a real Ollama model when running normally.

## Mini-Project — Banking FAQ Assistant

My mini-project is a banking FAQ assistant named Finley. It answers common questions about business loans, savings accounts, and wire transfers using a separate FAQ lookup tool. It also uses a local model for general questions that are not covered by the tool. The assistant is a mock system and does not access real bank accounts or perform transactions. Requests involving account changes or money transfers are referred to a bank representative because those actions require authorization.

### Week 11 Model Evaluation

When I asked whether the branch was open on Saturday, the model correctly answered that it was closed based on the instructions. When I asked for the mortgage interest rate, it said it did not have that information instead of making up a number. I decided to keep banking FAQ answers and requests involving account changes or money transfers handled by Python rules and tools. This is because those responses should be predictable and should not depend on what the model generates. The model is mainly used for general conversation and questions that are not covered by the existing tool.

## How to Run

Create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install Ollama from https://ollama.com/download and download the model:

```bash
ollama pull granite4.1:3b
```

Run the support chatbot:

```bash
python3 main.py
```

Run the banking assistant:

```bash
python3 my_main.py
```

Type `quit` to end either conversation.

## Other Programs

- `first_chat.py` — Makes a basic call to the local model.
- `no_memory.py` — Demonstrates separate calls without conversation history.
- `with_memory.py` — Demonstrates sending previous messages back to the model.
- `mock_model.py` — Provides predictable replies for testing.
- `ollama_model.py` — Connects Python to the local Ollama model.
- `echo_model.py` — Repeats the user's last message.
- `two_bots.py` — Demonstrates two chatbots with separate conversation histories.

## Project Files

- `chatbot.py` — Support chatbot that uses rules, tools, and a model.
- `order_tool.py` — Order-status lookup tool.
- `stock_tool.py` — Inventory lookup tool.
- `main.py` — Interactive support chatbot.
- `my_assistant.py` — Banking FAQ assistant.
- `my_tool.py` — Banking FAQ lookup tool.
- `my_main.py` — Interactive banking assistant.
- `tests/test_chatbot.py` — Support chatbot tests.
- `tests/test_my_assistant.py` — Banking assistant tests.
- `exercise1.md` — Week 10 OOP exercise answers.
- `week11_answers.md` — Week 11 exercise answers and model experiments.
- `ai_output.md` — Relevant generated class-code documentation.
- `requirements.txt` — Python dependencies.

## How to Test

Run the following commands:

```bash
ruff format .
ruff check .
pytest -v
```

The project has 27 passing tests: 15 for the support chatbot and 12 for the banking assistant. The tests use mock models and do not need Ollama running.

## AI Use Documentation

The project uses the instructor's provided examples for its original classes and model integration. Additional AI-assisted class code and explanations are recorded in `ai_output.md`.
