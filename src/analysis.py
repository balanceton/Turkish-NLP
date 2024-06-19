import spacy
from collections import defaultdict, Counter
from transformers import pipeline
from spacy.tokens import Token
import re

class TextAnalyzer:
    def __init__(self, model_path, stopwords, actions):
        self.nlp = spacy.load(model_path)
        self.stopwords = stopwords
        self.actions = actions
        self.human_like_actions = actions
        self.characters_found_by_spacy = set()
        self.characters_found_by_dep = set()
        self.processed_docs = []
        self.tokenizer = None
        self.morphology = None
        self.sa_pipeline = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")

    def analyze_text(self, text):
        preprocessed_text = preprocess_text(text)
        sentences = preprocessed_text.split(".")
        for sentence in sentences:
            doc = self.nlp(sentence)
            self.processed_docs.append(doc)
            self._extract_characters(doc)
        return self.processed_docs

    def _extract_characters(self, doc):
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                character = clean_entity_name(ent.text, self.actions, self.stopwords)
                if character and character not in self.stopwords:
                    self.characters_found_by_spacy.add(character)
                    for token in ent:
                        token._.entity_name = character

    def perform_sentiment_analysis(self, docs):
        relationships = {}
        person_queue = []
        for doc in docs:
            characters = []
            main_characters = set()
            for token in doc:
                entity_name = token._.entity_name if token._.entity_name else clean_entity_name(token.text, self.actions, self.stopwords)
                if entity_name in self.characters_found_by_spacy:
                    if token.dep_ == 'nsubj':
                        person_queue.insert(0, entity_name)
                        main_characters.add(entity_name)
                    characters.append(entity_name)
            sentiment = self.sa_pipeline(doc.text)
            relationships = self._update_relationships(main_characters, characters, sentiment, relationships)
        return relationships

    def _update_relationships(self, main_characters, characters, sentiment, relationships):
        calculated_relationships = set()
        for main_character in main_characters:
            for character in characters:
                if main_character != character:
                    char_pair = tuple(sorted((main_character, character)))
                    if char_pair in calculated_relationships:
                        continue
                    if char_pair not in relationships:
                        relationships[char_pair] = 0
                    relationships[char_pair] += sentiment[0]['score'] if sentiment[0]['label'] == 'positive' else -sentiment[0]['score']
                    calculated_relationships.add(char_pair)
        return relationships

    def get_filtered_characters(self, docs):
        word_counts = Counter()
        for doc in docs:
            for token in doc:
                if token._.entity_name in self.characters_found_by_spacy:
                    word_counts[token._.entity_name] += 1
        return {word for word, count in word_counts.items() if count >= 5}
