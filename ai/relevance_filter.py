# ai/relevance_filter.py

KEYWORDS = [
    "inflation", "interest", "rate hike", "central bank",
    "ECB", "Fed", "recession", "unemployment", "monetary policy"
]

def is_relevant(text: str, keywords=KEYWORDS) -> bool:
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)

# ai/relevance_filter.py

KEYWORDS = [
    "inflation", "interest", "rate hike", "central bank",
    "ECB", "Fed", "recession", "unemployment", "monetary policy"
]

def relevance_score(text: str, keywords=KEYWORDS) -> int:
    text_lower = text.lower()
    score = sum(1 for keyword in keywords if keyword.lower() in text_lower)
    return int((score / len(keywords)) * 100)

def is_relevant(text: str, threshold=20):
    return relevance_score(text) >= threshold
