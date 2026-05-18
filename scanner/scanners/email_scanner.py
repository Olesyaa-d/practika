import re

from scanner.base.base_scanner import BaseScanner

from scanner.results.email_result import EmailResult


class EmailScanner(BaseScanner):

    EMAIL_PATTERN = (
        r"[a-zA-Z0-9._%+-]+@"
        r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    )

    def scan(self, text):

        print("EMAIL SCANNER RUNNING")

        text = text.strip()

        emails = re.findall(
            self.EMAIL_PATTERN,
            text
        )

        emails = list(set(email.lower() for email in emails))

        return EmailResult(
            scanner_name="email_scanner",
            count=len(emails),
            emails=emails
        )
