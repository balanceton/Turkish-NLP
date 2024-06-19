import os
from src.preprocessing import preprocess_text, read_lines_to_set
from src.analysis import TextAnalyzer
from src.visualization import draw_graph

def main():
    data_dir = "data"
    text_file = os.path.join(data_dir, "esekokuz.txt")
    stopwords_file = os.path.join(data_dir, "turkish_stopwords.txt")
    actions_file = os.path.join(data_dir, "human_like_actions.txt")

    with open(text_file, "r", encoding="utf-8") as file:
        text = file.read()

    stopwords = read_lines_to_set(stopwords_file)
    actions = read_lines_to_set(actions_file)

    analyzer = TextAnalyzer("tr_core_news_trf", stopwords, actions)
    docs = analyzer.analyze_text(text)
    relationships = analyzer.perform_sentiment_analysis(docs)

    draw_graph(relationships, "Masalın Tamamı")

if __name__ == "__main__":
    main()
