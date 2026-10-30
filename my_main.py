# my_main.py
# Author: Ananda Ravinder

from my_assistant import BankingAssistant
from my_tool import BankFAQTool

FAQS = {
    "business loans": "Business loans require an application and credit review.",
    "savings accounts": "Our savings accounts are designed for customers who want to set money aside.",
    "wire transfers": "Wire transfers allow customers to send funds between bank accounts.",
}

faq_tool = BankFAQTool(FAQS)
assistant = BankingAssistant("Finley", faq_tool)

print("Type a message, or type quit to stop.")

user_message = input("You: ")

while user_message.lower() != "quit":
    print(f"{assistant.name}: {assistant.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(assistant.history)}")
