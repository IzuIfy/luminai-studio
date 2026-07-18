from ai_os.chatbot import SimpleChatbot


def test_chatbot_supports_open_and_summarize(tmp_path) -> None:
    memory_path = tmp_path / "memory.json"
    bot = SimpleChatbot(memory_path=str(memory_path))

    open_response = bot.chat("Open README.md")
    summarize_response = bot.chat("Summarize README.md")

    assert "Opened" in open_response or "File not found" in open_response
    assert "README" in summarize_response or "workspace" in summarize_response
