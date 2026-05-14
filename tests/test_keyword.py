import unittest

from scanner.keyword_scanner import KeywordScanner


class TestKeywordScanner(unittest.TestCase):

    def setUp(self):

        self.scanner = KeywordScanner()

    def test_find_keywords(self):

        text = """
        Документ секретно.
        Пароль: 12345
        CVV код
        """

        result = self.scanner.find_keywords(text)

        self.assertIn("секретно", result)

        self.assertIn("пароль", result)

        self.assertIn("cvv", result)

    def test_empty_text(self):

        result = self.scanner.find_keywords("")

        self.assertEqual(result, [])


if __name__ == "__main__":

    unittest.main()