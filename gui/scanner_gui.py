import tkinter as tk

from tkinter import (
    filedialog,
    scrolledtext,
    messagebox
)

from scanner.file_scanner import FileScanner


class ScannerGUI:

    def __init__(self):

        self.scanner = FileScanner()

        self.root = tk.Tk()

        self.root.title(
            "Поиск конфиденциальных данных"
        )

        self.root.geometry("800x600")

        self.open_button = tk.Button(
            self.root,
            text="Выбрать TXT файл",
            font=("Arial", 14),
            command=self.open_file
        )

        self.open_button.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Consolas", 11)
        )

        self.result_text.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

    def open_file(self):

        file_path = filedialog.askopenfilename(
            title="Выберите TXT файл",
            filetypes=[("Text files", "*.txt")]
        )

        if not file_path:
            return

        try:

            result = self.scanner.scan_file(file_path)

            self.show_results(
                file_path,
                result
            )

        except Exception as e:

            messagebox.showerror(
                "Ошибка",
                str(e)
            )

    def show_results(
        self,
        file_path,
        result
    ):

        emails = result["emails"]
        cards = result["cards"]
        keywords = result["keywords"]

        self.result_text.delete(1.0, tk.END)

        self.result_text.insert(
            tk.END,
            f"Файл:\n{file_path}\n\n"
        )

        # EMAIL
        self.result_text.insert(
            tk.END,
            f"EMAIL ({len(emails)}):\n"
        )

        self.result_text.insert(
            tk.END,
            "-" * 40 + "\n"
        )

        if emails:

            for email in emails:
                self.result_text.insert(
                    tk.END,
                    email + "\n"
                )

        else:
            self.result_text.insert(
                tk.END,
                "Не найдено\n"
            )

        self.result_text.insert(tk.END, "\n")

        # КАРТЫ
        self.result_text.insert(
            tk.END,
            f"НОМЕРА КАРТ ({len(cards)}):\n"
        )

        self.result_text.insert(
            tk.END,
            "-" * 40 + "\n"
        )

        if cards:

            for card in cards:
                self.result_text.insert(
                    tk.END,
                    card + "\n"
                )

        else:
            self.result_text.insert(
                tk.END,
                "Не найдено\n"
            )

        self.result_text.insert(tk.END, "\n")

        # КЛЮЧЕВЫЕ СЛОВА
        self.result_text.insert(
            tk.END,
            f"КОДОВЫЕ СЛОВА ({len(keywords)}):\n"
        )

        self.result_text.insert(
            tk.END,
            "-" * 40 + "\n"
        )

        if keywords:

            for word in keywords:
                self.result_text.insert(
                    tk.END,
                    word + "\n"
                )

        else:
            self.result_text.insert(
                tk.END,
                "Не найдено\n"
            )

    def run(self):

        self.root.mainloop()