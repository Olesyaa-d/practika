import unittest

from scanner.file_scanner import FileScanner


class TestFileScanner(unittest.TestCase):

    def setUp(self):

        self.scanner = FileScanner()

    def test_find_emails(self):

        text = """
        test@gmail.com
        admin@mail.ru
        invalid@email
        """

        result = self.scanner.find_emails(text)

        expected = [
            "test@gmail.com",
            "admin@mail.ru"
        ]

        self.assertEqual(
            sorted(result),
            sorted(expected)
        )

    def test_find_cards(self):

        text = """
        1111 2222 3333 4444
        5555-6666-7777-8888
        1234567812345678
        """

        result = self.scanner.find_cards(text)

        expected = [
            "1111 2222 3333 4444",
            "5555-6666-7777-8888",
            "1234567812345678"
        ]

        self.assertEqual(
            sorted(result),
            sorted(expected)
        )

    def test_find_keywords(self):

        text = """
        Документ секретно.
        Пароль: 12345
        CONFIDENTIAL
        """

        result = self.scanner.find_keywords(text)

        self.assertIn("секретно", result)

        self.assertIn("пароль", result)

    def test_normalize_text(self):

        text = "hello\n\nworld\t\t123"

        result = self.scanner.normalize_text(text)

        expected = "hello world 123"

        self.assertEqual(
            result,
            expected
        )

    def test_empty_text(self):

        text = ""

        emails = self.scanner.find_emails(text)

        cards = self.scanner.find_cards(text)

        keywords = self.scanner.find_keywords(text)

        self.assertEqual(emails, [])

        self.assertEqual(cards, [])

        self.assertEqual(keywords, [])


if __name__ == "__main__":

    unittest.main()