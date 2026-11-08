# my_main.py
# Author: Ananda Ravinder

from my_assistant import BankingAssistant
from my_tool import BankFAQTool
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Finley, a friendly banking FAQ assistant for a fictional bank.
Answer in one short sentence.
For this demo, customer service hours are Monday to Friday, 9 am to 5 pm.
The demo branch is closed on Saturdays and Sundays.
Only state facts provided in these instructions.
Do not invent account balances, interest rates, or banking policies.
If you do not know an answer, say you do not know and suggest asking a bank representative."""

FAQS = {
    "business loans": "Business loans require an application and credit review.",
    "savings accounts": "Savings accounts allow customers to save money and may earn interest.",
    "wire transfers": "Wire transfers send money electronically between bank accounts.",
}

faq_tool = BankFAQTool(FAQS)
model = OllamaModel(MODEL_NAME)

bot = BankingAssistant("Finley", INSTRUCTIONS, faq_tool, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")

while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")
