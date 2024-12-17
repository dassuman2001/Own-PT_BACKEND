import unittest
from app import chatbot

class TestChatbot(unittest.TestCase):
    def test_exact_match(self):
        self.assertEqual(
            chatbot("What is your name?"),
            "My full name is Suman Das."
        )
    
    def test_partial_match(self):
        self.assertEqual(
            chatbot("Tell me about your hobbies"),
            "I enjoy playing the guitar, singing, cricket, and online gaming."
        )

    def test_no_match(self):
        self.assertEqual(
            chatbot("What is the capital of India?"),
            "Sorry, I don't understand. Can you rephrase?"
        )

if __name__ == "__main__":
    unittest.main()
