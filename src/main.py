import os
import spacy
from text_analyzer import preprocess_text, read_lines_to_set, SentimentAnalyzer, CharacterExtractor, RelationshipAnalyzer, draw_graph

def main():
    data_dir = "data"
    reqs_dir = "language_based_reqs"
    text_file = os.path.join(data_dir, "esekokuz.txt")
    stopwords_file = os.path.join(reqs_dir, "turkish_stopwords.txt")
    actions_file = os.path.join(reqs_dir, "human_like_actions.txt")

    with open(text_file, "r", encoding="utf-8") as file:
        text = file.read()

    stopwords = read_lines_to_set(stopwords_file)
    actions = read_lines_to_set(actions_file)

    nlp = spacy.load("tr_core_news_trf")
    sentiment_analyzer = SentimentAnalyzer()
    character_extractor = CharacterExtractor(nlp, stopwords, actions)
    relationship_analyzer = RelationshipAnalyzer(stopwords, actions, character_extractor.characters_found_by_spacy)

    preprocessed_text = preprocess_text(text)
    sentences = preprocessed_text.split(".")

    docs = []
    for sentence in sentences:
        doc = nlp(sentence)
        character_extractor.extract_characters(doc)
        docs.append(doc)

    relationships = relationship_analyzer.analyze_relationships(docs, sentiment_analyzer)

    filtered_characters = character_extractor.get_filtered_characters(docs)
    print("Relationships:", relationships)
    print("Filtered Characters:", filtered_characters)

    draw_graph(relationships, "Masalın Tamamı")

if __name__ == "__main__":
    main()
