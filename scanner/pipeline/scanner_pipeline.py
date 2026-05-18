from scanner.scanners.email_scanner import EmailScanner
from scanner.scanners.card_scanner import CardScanner
from scanner.scanners.keyword_scanner import KeywordScanner


class ScannerPipeline:

    def __init__(self):

        self.scanners = [
            EmailScanner(),
            CardScanner(),
            KeywordScanner()
        ]

    def run(self, text):

        results = []

        for scanner in self.scanners:

            result = scanner.scan(text)

            results.append(result)

        return results