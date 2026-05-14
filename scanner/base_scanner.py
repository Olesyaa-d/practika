import re


class BaseScanner:

    def __init__(self, pattern):

        self.pattern = pattern

    def find_matches(
        self,
        text,
        flags=0
    ):

        matches = re.findall(
            self.pattern,
            text,
            flags
        )

        return list(set(matches))