
# Turkish-NLP

This project is focused on **Character Detection and Classification of Relationships in Turkish Texts**. It identifies characters in texts, analyzes relationships between these characters, and performs sentiment analysis. The results are visualized on a graph.

## Project Structure

Turkish-NLP/src/
│
├── init.py
├── character_extraction.py
├── main.py
├── preprocessing.py
├── relationships.py
├── sentiment_analysis.py
└── visualization.py

## Requirements

- Python 3.7 or higher
- Install the required Python packages using the `requirements.txt` file:

pip install -r requirements.txt

## Usage
1. Place the text files you want to analyze in the data folder. An example text file name is esekokuz.txt.
2. Create turkish_stopwords.txt and human_like_actions.txt files in the language_based_reqs folder and fill them with appropriate content.
3. Run the project: 
python Turkish-NLP/src/main.py
