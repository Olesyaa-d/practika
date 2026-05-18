import re

from scanner.base.base_scanner import BaseScanner

from scanner.results.keyword_result import KeywordResult


class KeywordScanner(BaseScanner):

    KEYWORDS = [
        "секретно",
        "конфиденциально",
        "конфеденциально",
        "пароль",
        "password",
        "login",
        "логин"
    ]

    PATTERN = (
        r"\b("
        + "|".join(KEYWORDS)
        + r")\b"
    )

    def scan(self, text):

        matches = re.findall(
            self.PATTERN,
            text,
            re.IGNORECASE
        )

        keywords = list(
            set(
                word.lower()
                for word in matches
            )
        )

        return KeywordResult(
            scanner_name="keyword_scanner",
            count=len(keywords),
            keywords=keywords
        )