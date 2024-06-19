# Text Analysis Project

## Overview

This project analyzes Turkish texts to identify characters and their relationships based on sentiment analysis.

## Setup

1. Clone the repository.
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Place your data files (`esekokuz.txt`, `turkish_stopwords.txt`, `human_like_actions.txt`) in the `data/` directory.

## Usage

Run the main script:
```
python main.py
```

## Directory Structure

```
project_root/
│
├── data/
│   ├── esekokuz.txt
│   ├── turkish_stopwords.txt
│   └── human_like_actions.txt
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── analysis.py
│   └── visualization.py
│
├── requirements.txt
├── README.md
└── main.py
```
