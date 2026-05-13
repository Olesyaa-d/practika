import re


class FileScanner:

    def __init__(self):

        self.email_pattern = (
            r"[a-zA-Z0-9._%+-]+@"
            r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        )

        self.card_pattern = r"""
        \b
        (?:\d{4}[\s-]?){3}\d{4}
        \b
        """

        self.keywords = [
            "секретно",
            "конфиденциально",
            "пароль",
            "password",
            "login",
            "логин"
        ]

    def read_file(self, file_path):

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def normalize_text(self, text):

        return re.sub(r"\s+", " ", text)

    def find_emails(self, text):

        emails = re.findall(
            self.email_pattern,
            text
        )

        return list(set(emails))

    def find_cards(self, text):

        cards = re.findall(
            self.card_pattern,
            text,
            re.VERBOSE
        )

        return list(set(cards))

    def find_keywords(self, text):

        found_keywords = []

        for word in self.keywords:

            pattern = rf"\b{re.escape(word)}\b"

            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):
                found_keywords.append(word)

        return list(set(found_keywords))

    def scan_file(self, file_path):

        text = self.read_file(file_path)

        normalized_text = self.normalize_text(text)

        return {
            "emails": self.find_emails(normalized_text),
            "cards": self.find_cards(normalized_text),
            "keywords": self.find_keywords(normalized_text)
        }