import os
from collections import Counter
from character_extraction import CharacterExtractor
from preprocess import preprocess_text
from relationships import RelationshipAnalyzer
from sentiment_analysis import SentimentAnalyzer
from visualization import draw_graph

def main():
    data_dir = "data"
    reqs_dir = "language_based_reqs"
    text_file = os.path.join(data_dir, "esekokuz.txt")
    stopwords_file = os.path.join(reqs_dir, "turkish_stopwords.txt")
    actions_file = os.path.join(reqs_dir, "human_like_actions.txt")

    with open(text_file, "r", encoding="utf-8") as file:
        text = file.read()

    character_extractor = CharacterExtractor()
    stopwords = character_extractor.load_words(stopwords_file)
    actions = character_extractor.load_words(actions_file)
    
    character_extractor.stopwords = stopwords

    sentiment_analyzer = SentimentAnalyzer()
    relationship_analyzer = RelationshipAnalyzer()

    preprocessed_text = preprocess_text(text)
    sentences = preprocessed_text.split(".")

    processed_docs, filtered_characters = character_extractor.extract_characters(sentences, actions)

    relationships = relationship_analyzer.analyze_relationships(processed_docs, filtered_characters, sentiment_analyzer)

    print("Relationships:", relationships)
    print("Filtered Characters:", filtered_characters)

    draw_graph(relationships, "Masalın Tamamı")

if __name__ == "__main__":
    main()