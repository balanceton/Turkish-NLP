# character_extraction.py
from .utils import clean_entity_name

class CharacterExtractor:
    def __init__(self, nlp, stopwords, actions):
        self.nlp = nlp
        self.stopwords = stopwords
        self.actions = actions
        self.characters_found_by_spacy = set()

    def extract_characters(self, doc):
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                character = clean_entity_name(ent.text, self.actions, self.stopwords)
                if character and character not in self.stopwords:
                    self.characters_found_by_spacy.add(character)
                    for token in ent:
                        token._.entity_name = character
        return self.characters_found_by_spacy
