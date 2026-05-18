import unittest

from scanner.scanners.email_scanner import EmailScanner


class TestEmailScanner(unittest.TestCase):

    def setUp(self):

        self.scanner = EmailScanner()

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

    def test_empty_text(self):

        result = self.scanner.find_emails("")

        self.assertEqual(result, [])


if __name__ == "__main__":

    unittest.main()