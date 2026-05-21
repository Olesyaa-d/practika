from collections import defaultdict

from scanner.preprocessing.text_tokenizer import TextTokenizer


class NaiveBayesClassifier:

    def __init__(self):
        self.tokenizer = TextTokenizer()

        self.documents = defaultdict(int)
        self.words = defaultdict(lambda: defaultdict(int))

    def train(self, documents):
        self.documents.clear()
        self.words.clear()

        for document in documents:
            document_type = document.type
            tokens = self.tokenizer.tokenize(document.text)

            self.documents[document_type] += 1

            for token in tokens:
                self.words[document_type][token] += 1

    def type_probability(self, document_type):
        total_documents = sum(self.documents.values())

        if total_documents == 0:
            return 0

        return self.documents[document_type] / total_documents

    def conditional_word_probability(self, word, document_type):
        word_count = self.words[document_type].get(word, 0)
        total_words = sum(self.words[document_type].values())

        if total_words == 0:
            return 0

        return (word_count + 1) / (total_words + 1)

    def predict(self, text):
        tokens = self.tokenizer.tokenize(text)

        scores = {}

        for document_type in self.documents.keys():
            probability = self.type_probability(document_type)

            for token in tokens:
                probability *= self.conditional_word_probability(
                    token,
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