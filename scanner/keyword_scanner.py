import re


class KeywordScanner:

    def __init__(self):

        self.keywords = [
            "секретно",
            "конфиденциально",
            "пароль",
            "password",
            "login",
            "логин"
        ]

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