import spacy
from spacy.tokens import Token
from zemberek.morphology import TurkishMorphology
from zemberek.tokenization import TurkishTokenizer
import re
import string
from collections import Counter

class CharacterExtractor:
    def __init__(self, stopwords=None):
        self.nlp = spacy.load("tr_core_news_trf")
        self.tokenizer = TurkishTokenizer.DEFAULT
        self.morphology = TurkishMorphology.create_with_defaults()
        Token.set_extension('entity_name', default=None, force=True)
        self.stopwords = stopwords if stopwords else set()

    def load_words(self, file_path):
        words = set()
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    word_list = line.split(",")
                    word_list = [word.strip() for word in word_list]
                    words.update(word_list)
        return words

    def clean_entity_name(self, name):
        cleaned_name = re.sub(r'[’\']\w*', '', name)
        cleaned_name = re.sub(f'^[{re.escape(string.punctuation)}\s]+|[{re.escape(string.punctuation)}\s]+$', '', cleaned_name)
        for stopword in self.stopwords:
            cleaned_name = re.sub(rf'\b{stopword}\b', '', cleaned_name)
        cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
        return cleaned_name.lower()

    def extract_characters(self, sentences, human_like_actions):
        processed_docs = []
        characters_found_by_spacy = set()
        characters_found_by_dep = set()

        for sentence in sentences:
            doc = self.nlp(sentence)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    character = self.clean_entity_name(ent.text)
                    if not character.isspace() and character != "" and character not in self.stopwords:
                        characters_found_by_spacy.add(character)
                        for token in ent:
                            token._.entity_name = character

            for token in doc:
                zemberek_lemma = None
                if token.is_space or token.is_punct:
                    continue
                if token.pos_ == "VERB":
                    text = token.text
                    zem_tokens = self.tokenizer.tokenize(text)
                    for zem_token in zem_tokens:
                        analysis = self.morphology.analyze(zem_token.normalized)
                        if analysis.analysis_results:
                            zemberek_lemma = analysis.analysis_results[0].item.root
                            break
                    if zemberek_lemma in human_like_actions:
                        for child in token.children:
                            if child.dep_ == "nsubj" and child.pos_ in ["PROPN", "PRON", "NOUN"] and child.lemma_ not in self.stopwords:
                                cleaned_name = self.clean_entity_name(child.lemma_)
                                if cleaned_name.isalpha() and cleaned_name not in self.stopwords:
                                    characters_found_by_dep.add(cleaned_name)
                                    child._.entity_name = cleaned_name

            processed_docs.append(doc)

        all_characters = characters_found_by_spacy.union(characters_found_by_dep)
        for doc in processed_docs:
            for token in doc:
                if token.lemma_.lower() in all_characters and token._.entity_name is None:
                    token._.entity_name = token.lemma_.lower()

        word_counts = Counter()
        for doc in processed_docs:
            for token in doc:
                if token._.entity_name in all_characters:
                    word_counts[token._.entity_name] += 1

        filtered_characters = {word for word, count in word_counts.items() if count >= 5}

        return processed_docs, filtered_characters
