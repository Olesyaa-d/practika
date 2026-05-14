import unittest

from scanner.card_scanner import CardScanner


class TestCardScanner(unittest.TestCase):

    def setUp(self):

        self.scanner = CardScanner()


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

    def test_empty_text(self):

        result = self.scanner.find_cards("")

        self.assertEqual(result, [])


if __name__ == "__main__":

    unittest.main()