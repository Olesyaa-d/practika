import re

from collections import defaultdict

from scanner.preprocessing.text_tokenizer import TextTokenizer


class NaiveBayesClassifier:

    EMAIL_PATTERN = (
        r"[a-zA-Z0-9._%+-]+@"
        r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    )

    CARD_PATTERN = r"""
    \b
    (?:\d{4}[\s-]?){3}\d{4}
    \b
    """

    SENSITIVE_KEYWORDS = [
        "секретно",
        "конфиденциально",
        "конфеденциально",
        "пароль",
        "password",
        "login",
        "логин",
        "доступ",
        "карта",
        "email"
    ]

    def __init__(self):
        self.tokenizer = TextTokenizer()

        self.documents = defaultdict(int)
        self.words = defaultdict(lambda: defaultdict(int))

    def extract_features(self, text):
        features = self.tokenizer.tokenize(text)

        emails = re.findall(
            self.EMAIL_PATTERN,
            text
        )

        cards = re.findall(
            self.CARD_PATTERN,
            text,
            re.VERBOSE
        )

        lowered_text = text.lower()

        found_keywords = [
            keyword
            for keyword in self.SENSITIVE_KEYWORDS
            if keyword in lowered_text
        ]

        for _ in emails:
            features.extend(["has_email"] * 10)

        for _ in cards:
            features.extend(["has_card"] * 15)

        for _ in found_keywords:
            features.extend(["has_sensitive_keyword"] * 8)

        return features

    def train(self, documents):
        self.documents.clear()
        self.words.clear()

        for document in documents:
            document_type = document.type

            features = self.extract_features(
                document.text
            )

            self.documents[document_type] += 1

            for feature in features:
                self.words[document_type][feature] += 1

    def type_probability(self, document_type):
        total_documents = sum(
            self.documents.values()
        )

        if total_documents == 0:
            return 0

        return (
            self.documents[document_type]
            /
            total_documents
        )

    def conditional_word_probability(self, word, document_type):
        word_count = self.words[document_type].get(
            word,
            0
        )

        total_words = sum(
            self.words[document_type].values()
        )

        if total_words == 0:
            return 0

        return (
            word_count + 1
        ) / (
            total_words + 1
        )

    def predict(self, text):
        features = self.extract_features(text)

        scores = {}

        for document_type in self.documents.keys():
            probability = self.type_probability(
                document_type
            )

            for feature in features:
                probability *= self.conditional_word_probability(
                    feature,
                    document_type
                )

            scores[document_type] = probability

        if not scores:
            return {
                "predicted_type": None,
                "scores": {}
            }

        predicted_type = max(
            scores,
            key=scores.get
        )

        return {
            "predicted_type": predicted_type,
            "scores": scores
        }