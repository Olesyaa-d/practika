import re

from scanner.base_scanner import BaseScanner


class CardScanner(BaseScanner):

    def __init__(self):

        pattern = r"""
        \b
        (?:\d{4}[\s-]?){3}\d{4}
        \b
        """

        super().__init__(pattern)

    def find_cards(self, text):

        return self.find_matches(
            text,
            re.VERBOSE
        )