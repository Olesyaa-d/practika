import re

from scanner.base.base_scanner import BaseScanner

from scanner.results.card_result import CardResult


class CardScanner(BaseScanner):

    CARD_PATTERN = r"""
    \b
    (?:\d{4}[\s-]?){3}\d{4}
    \b
    """

    def scan(self, text):

        cards = re.findall(
            self.CARD_PATTERN,
            text,
            re.VERBOSE
        )

        cards = list(set(cards))

        return CardResult(
            scanner_name="card_scanner",
            count=len(cards),
            cards=cards
        )