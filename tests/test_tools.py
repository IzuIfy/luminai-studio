from ai_os.chatbot import SimpleChatbot


def test_chatbot_supports_reminders_and_search(tmp_path) -> None:
    memory_path = tmp_path / "memory.json"
    bot = SimpleChatbot(memory_path=str(memory_path))

    reminder_response = bot.chat("Reminder: call mom")
    search_response = bot.chat("Search README")

    assert "Reminder added" in reminder_response
    assert "README" in search_response or "No files matched" in search_response
