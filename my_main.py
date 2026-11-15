# my_main.py
# Author: Ananda Ravinder

from banking_toolbox import BankingToolbox
from contact_change_queue import ContactChangeQueue
from my_assistant import BankingAssistant
from my_tool import BankFAQTool
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Finley, a banking FAQ assistant for a fictional bank.
Answer in one short sentence.
Customer service hours are Monday to Friday, 9 am to 5 pm.
The branch is closed on Saturdays and Sundays.
Only state facts from these instructions or tool results.
If the customer only says hello, greet them and ask how you can help.
Use the FAQ tool when the customer asks about a banking topic.
For contact preference changes, ask for the customer ID and the new contact method.
Only request a contact change after the customer provides both details.
Contact changes must be approved by staff before they take effect.
Do not invent customer IDs, account information, or banking policies.
If you do not know an answer, say so and suggest a bank representative."""

FAQS = {
    "business loans": "Business loans require an application and credit review.",
    "savings accounts": "Savings accounts allow customers to save money and may earn interest.",
    "wire transfers": "Wire transfers send money electronically between bank accounts.",
}

CUSTOMERS = {
    "C100": {"contact_method": "phone"},
    "C101": {"contact_method": "email"},
}

faq_tool = BankFAQTool(FAQS)
contact_queue = ContactChangeQueue(CUSTOMERS)
tools = BankingToolbox(faq_tool, contact_queue)

model = OllamaModel(MODEL_NAME)
bot = BankingAssistant("Finley", INSTRUCTIONS, tools, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")

while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")

print("Staff review")
for request in contact_queue.waiting():
    number = request["number"]
    customer_id = request["customer_id"]
    new_method = request["new_method"]

    print(f"Request {number}: {customer_id} to {new_method}")

    answer = input("Approve? yes or no: ")

    if answer == "yes":
        print(contact_queue.approve(number))
    else:
        print(contact_queue.reject(number))

print("Customer contact preferences")
for customer_id in CUSTOMERS:
    print(customer_id, CUSTOMERS[customer_id]["contact_method"])
