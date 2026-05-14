import re

from scanner.base_scanner import BaseScanner


class KeywordScanner(BaseScanner):

    def __init__(self):

        keywords = [
            "секретно",
            "конфиденциально",
            "пароль",
            "password",
            "login",
            "логин"
        ]

        pattern = (
            r"\b("
            + "|".join(keywords)
            + r")\b"
        )

        super().__init__(pattern)

    def find_keywords(self, text):

        matches = self.find_matches(
            text,
            re.IGNORECASE
        )

        return [word.lower() for word in matches]