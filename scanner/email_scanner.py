import re


class EmailScanner:

    def __init__(self):

        self.email_pattern = (
            r"[a-zA-Z0-9._%+-]+@"
            r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        )

    def find_emails(self, text):

        emails = re.findall(
            self.email_pattern,
            text
        )

        return list(set(emails))