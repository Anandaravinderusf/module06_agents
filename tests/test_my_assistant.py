# tests/test_my_assistant.py
# Author: Ananda Ravinder

from unittest.mock import Mock

from banking_toolbox import BankingToolbox
from contact_change_queue import ContactChangeQueue
from fake_model import FakeModel
from my_assistant import BankingAssistant
from my_tool import BankFAQTool

FAQS = {
    "business loans": "Business loans require an application and credit review.",
    "savings accounts": "Savings accounts allow customers to save money and may earn interest.",
    "wire transfers": "Wire transfers send money electronically between bank accounts.",
}


def make_bot(model):
    """Create a banking assistant with fresh mock data."""
    customers = {
        "C100": {"contact_method": "phone"},
        "C101": {"contact_method": "email"},
    }

    faq_tool = BankFAQTool(FAQS)
    queue = ContactChangeQueue(customers)
    tools = BankingToolbox(faq_tool, queue)

    return BankingAssistant("Finley", "Be friendly.", tools, model)


def ask_for_tool(name, arguments):
    """Create a tool request for FakeModel."""
    return {"tool": name, "arguments": arguments}


def test_greeting():
    bot = make_bot(FakeModel([{"text": "Hello! How can I help?"}]))
    assert bot.respond("hello") == "Hello! How can I help?"


def test_faq_lookup():
    model = FakeModel(
        [
            ask_for_tool("look_up_faq", {"topic": "business loans"}),
            {"text": FAQS["business loans"]},
        ]
    )
    bot = make_bot(model)

    assert bot.respond("Do you offer business loans?") == FAQS["business loans"]
    assert bot.history[1]["role"] == "tool"
    assert bot.history[1]["tool_name"] == "look_up_faq"


def test_unknown_banking_topic():
    model = FakeModel(
        [
            ask_for_tool("look_up_faq", {"topic": "mortgages"}),
            {"text": "I don't have information about mortgages."},
        ]
    )
    bot = make_bot(model)

    bot.respond("Can you explain mortgages?")
    assert "don't have information" in bot.history[1]["content"]


def test_made_up_faq_topic_is_refused():
    model = FakeModel(
        [
            ask_for_tool("look_up_faq", {"topic": "wire transfers"}),
            {"text": "Please ask about a banking topic."},
        ]
    )
    bot = make_bot(model)

    bot.respond("Tell me about savings accounts")
    assert "has not mentioned" in bot.history[1]["content"]


def test_contact_change_waits_for_staff():
    model = FakeModel(
        [
            ask_for_tool(
                "request_contact_change",
                {"customer_id": "C100", "new_method": "email"},
            ),
            {"text": "Your request was sent to staff."},
        ]
    )
    bot = make_bot(model)

    bot.respond("My ID is C100. Change my contact preference to email.")

    assert len(bot.tools.contact_queue.waiting()) == 1
    assert bot.tools.contact_queue.customers["C100"]["contact_method"] == "phone"


def test_made_up_customer_id_is_refused():
    model = FakeModel(
        [
            ask_for_tool(
                "request_contact_change",
                {"customer_id": "C101", "new_method": "email"},
            ),
            {"text": "Please provide your customer ID."},
        ]
    )
    bot = make_bot(model)

    bot.respond("My ID is C100. Change my contact preference to email.")

    assert "has not provided" in bot.history[1]["content"]
    assert bot.tools.contact_queue.waiting() == []


def test_made_up_contact_method_is_refused():
    model = FakeModel(
        [
            ask_for_tool(
                "request_contact_change",
                {"customer_id": "C100", "new_method": "email"},
            ),
            {"text": "Which contact method would you like?"},
        ]
    )
    bot = make_bot(model)

    bot.respond("My customer ID is C100. Change my contact preference.")

    assert "has not requested" in bot.history[1]["content"]
    assert bot.tools.contact_queue.waiting() == []


def test_missing_contact_details():
    model = FakeModel(
        [
            ask_for_tool(
                "request_contact_change",
                {"customer_id": "", "new_method": "email"},
            ),
            {"text": "Please provide your customer ID."},
        ]
    )
    bot = make_bot(model)

    bot.respond("Change my contact preference to email")

    assert "both needed" in bot.history[1]["content"]
    assert bot.tools.contact_queue.waiting() == []


def test_staff_approval_only_changes_once():
    model = FakeModel(
        [
            ask_for_tool(
                "request_contact_change",
                {"customer_id": "C100", "new_method": "email"},
            ),
            {"text": "Sent to staff."},
        ]
    )
    bot = make_bot(model)
    bot.respond("My ID is C100. Change my contact preference to email.")

    queue = bot.tools.contact_queue

    assert queue.customers["C100"]["contact_method"] == "phone"
    assert queue.approve(1) == "Request 1 approved."
    assert queue.customers["C100"]["contact_method"] == "email"
    assert queue.approve(1) == "Request 1 is already approved."


def test_rejected_request_changes_nothing():
    model = FakeModel(
        [
            ask_for_tool(
                "request_contact_change",
                {"customer_id": "C100", "new_method": "email"},
            ),
            {"text": "Sent to staff."},
        ]
    )
    bot = make_bot(model)
    bot.respond("My ID is C100. Change my contact preference to email.")

    queue = bot.tools.contact_queue
    assert queue.reject(1) == "Request 1 rejected."
    assert queue.customers["C100"]["contact_method"] == "phone"
    assert queue.approve(1) == "Request 1 is already rejected."


def test_money_transfer_goes_to_human():
    model = FakeModel([])
    bot = make_bot(model)

    assert "bank representative" in bot.respond("Please transfer money")
    assert model.calls == 0


def test_account_change_goes_to_human():
    model = FakeModel([])
    bot = make_bot(model)

    assert "bank representative" in bot.respond("Please change my account")
    assert model.calls == 0


def test_unknown_tool_is_refused():
    model = FakeModel(
        [
            ask_for_tool("delete_account", {"customer_id": "C100"}),
            {"text": "That action is unavailable."},
        ]
    )
    bot = make_bot(model)

    bot.respond("Delete my account C100")
    assert bot.history[1]["content"] == "There is no tool named delete_account."


def test_model_without_answer():
    model = Mock()
    model.decide.return_value = None
    bot = make_bot(model)

    assert "can't answer" in bot.respond("hello")
    model.decide.assert_called_once()


def test_tool_loop_stops_after_three_rounds():
    request = ask_for_tool("look_up_faq", {"topic": "business loans"})
    bot = make_bot(FakeModel([request, request, request]))

    reply = bot.respond("Tell me about business loans")

    assert "bank representative" in reply
    assert len(bot.history) == 5


def test_separate_conversation_histories():
    first = make_bot(FakeModel([{"text": "Hello!"}]))
    second = make_bot(FakeModel([{"text": "Hi!"}]))

    first.respond("hello")

    assert len(first.history) == 2
    assert len(second.history) == 0
