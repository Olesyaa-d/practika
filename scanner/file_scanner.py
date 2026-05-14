import re

from scanner.email_scanner import EmailScanner
from scanner.card_scanner import CardScanner
from scanner.keyword_scanner import KeywordScanner


class FileScanner:

    def __init__(self):

        self.email_scanner = EmailScanner()

        self.card_scanner = CardScanner()

        self.keyword_scanner = KeywordScanner()

    def read_file(self, file_path):

        with open(file_path, "r", encoding="utf-8") as file:

            return file.read()

    def normalize_text(self, text):

        return re.sub(r"\s+", " ", text)

    def scan_file(self, file_path):

        text = self.read_file(file_path)

        normalized_text = self.normalize_text(text)

        emails = self.email_scanner.find_emails(
            normalized_text
        )

        cards = self.card_scanner.find_cards(
            normalized_text
        )

        keywords = self.keyword_scanner.find_keywords(
            normalized_text
        )

        return {
            "emails": emails,
            "cards": cards,
            "keywords": keywords
        }