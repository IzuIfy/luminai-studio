from ai_os.chatbot import SimpleChatbot


def test_chatbot_remembers_names_and_notes(tmp_path) -> None:
    memory_path = tmp_path / "memory.json"
    bot = SimpleChatbot(memory_path=str(memory_path))

    bot.chat("My name is Ada")
    bot.chat("Please note that I like hiking")

    assert bot.memory["name"] == "Ada"
    assert bot.notes == ["I like hiking"]
    assert memory_path.exists()
