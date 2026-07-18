"""Simple command-line entry point for the starter AI operating system."""

from __future__ import annotations

from ai_os.chatbot import SimpleChatbot


def main() -> None:
    bot = SimpleChatbot()
    print("AI OS starter ready. Type 'exit' to quit.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        print(f"Assistant: {bot.chat(user_input)}")


if __name__ == "__main__":
    main()
