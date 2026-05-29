import unittest

from scanner.context.analysis_context import AnalysisContext
from scanner.scanners.card_scanner import CardScanner


class TestCardScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = CardScanner()

    def make_context(self, text):
        return AnalysisContext(
            raw_text=text,
            normalized_text=text,
            tokens=[]
        )

    def test_find_cards(self):
        text = """
        1111 2222 3333 4444
        5555-6666-7777-8888
        1234567812345678
        """

        result = self.scanner.scan(
            self.make_context(text)
        )

        self.assertEqual(result.count, 3)

    def test_empty_text(self):
        result = self.scanner.scan(
            self.make_context("")
        )

        self.assertEqual(result.count, 0)
        self.assertEqual(result.cards, [])


if __name__ == "__main__":
    unittest.main()