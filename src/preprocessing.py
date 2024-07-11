import re
import string

def preprocess_text(self, text):
        text = text.replace("’", "'")
        text = text.replace("“", '"')
        text = text.replace("”", '"')
        text = re.sub(r"'(\s+)", "'", text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

def read_lines_to_set(filepath):
    items = set()
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                items.update(line.split(","))
    return {item.strip() for item in items}
