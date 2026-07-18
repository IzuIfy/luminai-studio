from ai_os.chatbot import SimpleChatbot


def test_chatbot_supports_profile_and_tasks(tmp_path) -> None:
    memory_path = tmp_path / "memory.json"
    bot = SimpleChatbot(memory_path=str(memory_path))

    bot.chat("My name is Ada")
    bot.chat("Please note that I like hiking")
    bot.chat("Task: review project notes")

    assert bot.profile["name"] == "Ada"
    assert bot.notes == ["I like hiking"]
    assert bot.tasks[0]["task"] == "review project notes"
    assert memory_path.exists()
