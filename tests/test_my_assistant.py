# tests/test_my_assistant.py
# Author: Ananda Ravinder

from unittest.mock import Mock

from mock_model import MockModel
from my_assistant import BankingAssistant
from my_tool import BankFAQTool

FAQS = {
    "business loans": "Business loans require an application and credit review.",
    "savings accounts": "Savings accounts allow customers to save money and may earn interest.",
    "wire transfers": "Wire transfers send money electronically between bank accounts.",
}


def make_bot(model=None):
    """Build a banking assistant with mock FAQ data."""
    faq_tool = BankFAQTool(FAQS)
    if model is None:
        model = MockModel()
    return BankingAssistant("Finley", "Be friendly.", faq_tool, model)


def make_bot_without_model_answer():
    """Create a model that returns no answer."""
    model = Mock()
    model.reply.return_value = None
    return make_bot(model), model


def test_greeting():
    bot = make_bot()
    assert bot.respond("hello") == "Hello! How can I help you today?"


def test_business_loans():
    bot = make_bot()
    assert bot.respond("Do you offer business loans?") == FAQS["business loans"]


def test_savings_accounts():
    bot = make_bot()
    assert bot.respond("Tell me about savings accounts") == FAQS["savings accounts"]


def test_wire_transfers():
    bot = make_bot()
    assert bot.respond("How do wire transfers work?") == FAQS["wire transfers"]


def test_account_change_handoff():
    bot = make_bot()
    assert "bank representative" in bot.respond("Please change my account details")


def test_money_transfer_handoff():
    bot = make_bot()
    assert "bank representative" in bot.respond("Please transfer money")


def test_unknown_question_uses_model():
    bot = make_bot()
    assert "not sure" in bot.respond("Can you help me with something else?")


def test_safe_reply_when_model_has_no_answer():
    bot, model = make_bot_without_model_answer()
    assert "can't answer" in bot.respond("hello")
    model.reply.assert_called_once()


def test_faq_works_without_model():
    bot, model = make_bot_without_model_answer()
    assert bot.respond("Do you offer business loans?") == FAQS["business loans"]
    model.reply.assert_not_called()


def test_handoff_works_without_model():
    bot, model = make_bot_without_model_answer()
    assert "bank representative" in bot.respond("Please change my account details")
    model.reply.assert_not_called()


def test_conversation_history():
    bot = make_bot()
    bot.respond("hello")
    assert len(bot.history) == 2
    assert bot.history[0]["role"] == "user"
    assert bot.history[1]["role"] == "assistant"


def test_separate_conversation_histories():
    first_bot = make_bot()
    second_bot = make_bot()

    first_bot.respond("hello")

    assert len(first_bot.history) == 2
    assert len(second_bot.history) == 0
