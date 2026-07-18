import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_os.chatbot import SimpleChatbot


class SimpleChatbotTests(unittest.TestCase):
    def setUp(self):
        self.bot = SimpleChatbot()

    def test_chatbot_greets_the_user(self):
        response = self.bot.chat("hello")
        self.assertIn("hello", response.lower())

    def test_chatbot_remembers_facts(self):
        response = self.bot.chat("Please remember that my favorite color is blue")
        self.assertIn("remember", response.lower())
        self.assertEqual(self.bot.memory["favorite color"], "blue")

    def test_chatbot_recalls_stored_facts(self):
        self.bot.chat("Please remember that my favorite color is blue")
        response = self.bot.chat("What do you remember?")
        self.assertIn("favorite color", response.lower())
        self.assertIn("blue", response.lower())


if __name__ == "__main__":
    unittest.main()
