import re
from collections import defaultdict
from character_extraction import CharacterExtractor

class RelationshipAnalyzer:
    def __init__(self):
        self.char_extractor = CharacterExtractor()

    def check_double_quotes(self, sentence):
        return len(re.findall(r'"', sentence)) == 2

    def has_nsubj(self, doc):
        for token in doc:
            if token.dep_ == 'nsubj':
                return True
        return False

    def find_relationships(self, main_characters, characters, sentiment, relationships):
        calculated_relationships = set()
        for main_character in main_characters:
            for character in characters:
                if main_character != character:
                    char1 = main_character
                    char2 = character
                    char_pair = (min(char1, char2), max(char1, char2))
                    if char_pair in calculated_relationships:
                        continue
                    if char_pair not in relationships:
                        relationships[char_pair] = 0
                    if sentiment[0]['label'] == 'negative':
                        relationships[char_pair] -= sentiment[0]['score']
                    else:
                        relationships[char_pair] += sentiment[0]['score']
                    calculated_relationships.add(char_pair)
        return relationships

    def analyze_relationships(self, docs, filtered_characters, sentiment_analyzer):
        person_queue = []
        relationships = {}
        for doc in docs:
            characters = []
            main_characters = set()
            has_speech = self.check_double_quotes(doc.text)
            flag = self.has_nsubj(doc)
            for token in doc:
                entity_name = token._.entity_name if token._.entity_name else self.char_extractor.clean_entity_name(token.text)
                if entity_name in filtered_characters:
                    if token.dep_ == 'nsubj':
                        person_queue.insert(0, entity_name)
                        main_characters.add(entity_name)
                    if entity_name not in characters:
                        characters.append(entity_name)
                if token.dep_ == 'ROOT' and token.pos_ == 'VERB' and flag and person_queue:
                    main_characters.add(person_queue[-1])
            if characters and main_characters:
                sentiment = sentiment_analyzer.analyze(doc.text)
                relationships = self.find_relationships(main_characters, characters, sentiment, relationships)
        return relationships
