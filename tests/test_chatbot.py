import unittest

from chatbot import FALLBACK_RESPONSE, get_response


class GeneralKnowledgeChatbotTests(unittest.TestCase):
    def test_greeting(self):
        self.assertIn("Aspire Bot", get_response("Hello"))

    def test_country_specific_capitals(self):
        self.assertEqual(
            get_response("What is the capital of France?"),
            "The capital of France is Paris.",
        )
        self.assertEqual(
            get_response("What is the capital of India?"),
            "The capital of India is New Delhi.",
        )

    def test_science_question(self):
        self.assertIn("Jupiter", get_response("Which is the largest planet?"))

    def test_unknown_question_uses_fallback(self):
        self.assertEqual(
            get_response("Who won a made-up tournament on Mars?"),
            FALLBACK_RESPONSE,
        )

    def test_ambiguous_question_uses_fallback(self):
        self.assertEqual(get_response("What is the capital?"), FALLBACK_RESPONSE)


if __name__ == "__main__":
    unittest.main()
