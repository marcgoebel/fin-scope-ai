# ai/relevance_filter.py

KEYWORDS = [
    "inflation", "interest", "rate hike", "central bank",
    "ECB", "Fed", "recession", "unemployment", "monetary policy"
]

def is_relevant(text: str, keywords=KEYWORDS) -> bool:
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)
