# relationships.py
from collections import Counter

class RelationshipAnalyzer:
    def __init__(self, stopwords, actions, characters_found_by_spacy):
        self.stopwords = stopwords
        self.actions = actions
        self.characters_found_by_spacy = characters_found_by_spacy

    def analyze_relationships(self, docs, sentiment_analyzer):
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
            sentiment = sentiment_analyzer.analyze(doc.text)
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
