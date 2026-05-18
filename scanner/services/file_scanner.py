import re

from scanner.pipeline.scanner_pipeline import (
    ScannerPipeline
)


class FileScanner:

    def __init__(self, pipeline):

        self.pipeline = pipeline

    def read_file(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    def normalize_text(self, text):

        return re.sub(
            r"\s+",
            " ",
            text
        )

    def scan_file(self, file_path):

        text = self.read_file(file_path)

        normalized_text = self.normalize_text(text)

        return self.pipeline.run(
            normalized_text
        )