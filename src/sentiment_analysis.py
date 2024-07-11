from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.sa_pipeline = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")

    def analyze(self, text):
        return self.sa_pipeline(text)
