class ScannerPipeline:

    def __init__(self):
        # список всех сканеров
        self.scanners = []

    def add_scanner(self, scanner):
        """
        Добавляет сканер в pipeline
        """
        self.scanners.append(scanner)

    def run(self, text: str):
        """
        Запускает все сканеры и возвращает результаты
        """

        if not self.scanners:
            print("WARNING: pipeline has no scanners")

        results = []

        for scanner in self.scanners:

            try:
                result = scanner.scan(text)

                if result is not None:
                    results.append(result)

            except Exception as e:
                print(f"Scanner error in {scanner}: {e}")

        return results