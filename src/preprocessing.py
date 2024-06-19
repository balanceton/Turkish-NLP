import re
import string

def preprocess_text(text):
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"'(\s+)", "'", text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_entity_name(name, turkish_conjunctions, turkish_stopwords):
    cleaned_name = re.sub(r'[’\']\w*', '', name)
    cleaned_name = re.sub(f'^[{re.escape(string.punctuation)}\s]+|[{re.escape(string.punctuation)}\s]+$', '', cleaned_name)
    for conjunction in turkish_conjunctions:
        cleaned_name = re.sub(rf'\b{conjunction}\b', '', cleaned_name)
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
    return cleaned_name.lower()

def read_lines_to_set(filepath):
    items = set()
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                items.update(line.split(","))
    return {item.strip() for item in items}
