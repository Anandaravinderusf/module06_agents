from my_assistant import BankingAssistant
from my_tool import BankFAQTool


def make_assistant():
    """Create a fresh banking FAQ assistant for each test."""
    faqs = {
        "business loans": "Business loans require an application and credit review.",
        "savings accounts": "Savings accounts help customers set money aside.",
    }
    return BankingAssistant("Finley", BankFAQTool(faqs))


def test_tool_finds_known_topic():
    tool = BankFAQTool({"business loans": "Application required."})
    assert tool.find_topic("Tell me about business loans") == "business loans"


def test_tool_returns_none_for_unknown_topic():
    tool = BankFAQTool({"business loans": "Application required."})
    assert tool.find_topic("What about mortgages?") is None


def test_assistant_answers_banking_faq():
    assistant = make_assistant()
    reply = assistant.respond("Do you offer business loans?")
    assert "application and credit review" in reply


def test_unknown_faq_gets_helpful_reply():
    assistant = make_assistant()
    reply = assistant.respond("What about mortgages?")
    assert "don't have that information" in reply


def test_sensitive_request_goes_to_human():
    assistant = make_assistant()
    reply = assistant.respond("Please change my account details")
    assert "bank representative" in reply


def test_unhandled_request_gets_safe_reply():
    assistant = make_assistant()
    reply = assistant.respond("Play some music")
    assert "not sure" in reply


def test_conversation_history_records_both_sides():
    assistant = make_assistant()
    assistant.respond("hello")
    assert len(assistant.history) == 2
    assert assistant.history[0]["role"] == "user"
    assert assistant.history[1]["role"] == "assistant"
