import re


class CardScanner:

    def __init__(self):

        self.card_pattern = r"""
        \b
        (?:\d{4}[\s-]?){3}\d{4}
        \b
        """

    def find_cards(self, text):

        cards = re.findall(
            self.card_pattern,
            text,
            re.VERBOSE
        )

        return list(set(cards))