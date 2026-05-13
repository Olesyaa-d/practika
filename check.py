import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


def open_file():
    file_path = filedialog.askopenfilename(
        title="Выберите TXT файл",
        filetypes=[("Text files", "*.txt")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

    
        normalized_text = re.sub(r"\s+", " ", text)


        keywords = [
            "секретно",
            "конфиденциально",
            "пароль",
            "password",
            "login",
            "логин"
        ]

        found_keywords = []

        for word in keywords:
            pattern = rf"\b{re.escape(word)}\b"

            if re.search(pattern, normalized_text, re.IGNORECASE):
                found_keywords.append(word)

        found_keywords = list(set(found_keywords))

        keyword_count = len(found_keywords)

       
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        emails = re.findall(email_pattern, normalized_text)

        emails = list(set(emails))

        email_count = len(emails)

       
        card_pattern = r"""
        \b
        (?:\d{4}[\s-]?){3}\d{4}
        \b
        """

        cards = re.findall(card_pattern, normalized_text, re.VERBOSE)

        cards = list(set(cards))

        card_count = len(cards)


        result_text.delete(1.0, tk.END)

        result_text.insert(tk.END, f"Файл:\n{file_path}\n\n")

        result_text.insert(
            tk.END,
            f"EMAIL ({email_count}):\n"
        )
        result_text.insert(tk.END, "-" * 40 + "\n")

        if emails:
            for email in emails:
                result_text.insert(tk.END, email + "\n")
        else:
            result_text.insert(tk.END, "Не найдено\n")

        result_text.insert(tk.END, "\n")

        result_text.insert(
            tk.END,
            f"НОМЕРА КАРТ ({card_count}):\n"
        )
        result_text.insert(tk.END, "-" * 40 + "\n")

        if cards:
            for card in cards:
                result_text.insert(tk.END, card + "\n")
        else:
            result_text.insert(tk.END, "Не найдено\n")

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

    result_text.insert(tk.END, "\n")

    result_text.insert(
        tk.END,
        f"КЛЮЧЕВЫЕ СЛОВА ({keyword_count}):\n"
    )

    result_text.insert(tk.END, "-" * 40 + "\n")

    if found_keywords:
        for word in found_keywords:
            result_text.insert(tk.END, word + "\n")
    else:
        result_text.insert(tk.END, "Не найдено\n")


root = tk.Tk()
root.title("Поиск Email и Номеров Карт")
root.geometry("800x600")

open_button = tk.Button(
    root,
    text="Выбрать TXT файл",
    font=("Impact", 16),
    command=open_file
)

open_button.pack(pady=10)

result_text = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Consolas", 11)
)

result_text.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()