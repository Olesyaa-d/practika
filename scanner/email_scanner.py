from scanner.base_scanner import BaseScanner


class EmailScanner(BaseScanner):

    def __init__(self):

        pattern = (
            r"[a-zA-Z0-9._%+-]+@"
            r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        )

        super().__init__(pattern)

    def find_emails(self, text):

        return self.find_matches(text)