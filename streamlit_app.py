# streamlit_app.py

import streamlit as st
from news.news_scraper import get_finance_news
from ai.relevance_filter import is_relevant
from ai.relevance_filter import relevance_score
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from ai.relevance_filter import KEYWORDS

def score_color(score):
    if score >= 70:
        return "green"
    elif score >= 40:
        return "orange"
    else:
        return "red"

st.set_page_config(page_title="FinScope AI", layout="wide")
st.title("🧠 FinScope AI – Smart Finance News Filter")
topics = [
    "inflation", "interest rate", "rate hike", "central bank", 
    "ECB", "Fed", "recession", "unemployment", "monetary policy"
]

selected_topics = st.multiselect(
    "📚 Select Topics to Focus On (optional)",
    options=topics,
    default=[]
)

if st.button("🔄 Refresh News Feed"):
    st.experimental_rerun()
score_threshold = st.slider("🎯 Minimum Relevance Score", min_value=0, max_value=100, value=30)
st.markdown("This app fetches the latest financial news and prepares it for AI-based filtering. 🚀")

# News anzeigen
with st.spinner('🔄 Scraping finance news...'):
    news = get_finance_news()
filtered_news = [item for item in news if is_relevant(item["summary"])]

# Scored News
scored_news = []
for item in news:
    score = relevance_score(item["summary"])
    if score >= score_threshold:
        item["score"] = score
        scored_news.append(item)
if scored_news:
    export_df = pd.DataFrame(scored_news)[["title", "score", "summary", "link"]]
    csv = export_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered News as CSV",
        data=csv,
        file_name='filtered_finance_news.csv',
        mime='text/csv'
    )
# Scored News, angepasst an ausgewählte Topics
scored_news = []
for item in news:
    text = item["summary"].lower()
    score = relevance_score(text)

    if selected_topics:
        if any(topic in text for topic in selected_topics):
            if score >= score_threshold:
                item["score"] = score
                scored_news.append(item)
    else:
        if score >= score_threshold:
            item["score"] = score
            scored_news.append(item)

# Verteilung der Scores
score_values = [item["score"] for item in scored_news]
if score_values:
    st.subheader("📊 Relevance Score Distribution")

    fig, ax = plt.subplots()
    ax.hist(score_values, bins=range(0, 110, 10), edgecolor='black')
    ax.set_xlabel("Relevance Score (%)")
    ax.set_ylabel("Number of Articles")
    ax.set_title("Distribution of News Relevance Scores")

    st.pyplot(fig)

# WordCloud generieren
if scored_news:
    all_text = " ".join([item["summary"] for item in scored_news])

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

    st.subheader("☁️ WordCloud of Filtered News Summaries")

    fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
    ax_wc.imshow(wordcloud, interpolation='bilinear')
    ax_wc.axis('off')

    st.pyplot(fig_wc)
from collections import Counter
import re

# Alle Wörter aus den Zusammenfassungen sammeln
all_text = " ".join([item["summary"] for item in scored_news])
words = re.findall(r'\b\w+\b', all_text.lower())

# Optional: Stoppwörter ignorieren
stopwords = set(["the", "and", "to", "in", "of", "for", "on", "with", "a", "is", "by", "as", "at", "from", "that", "this"])
filtered_words = [word for word in words if word not in stopwords]

# Häufigstes Wort finden
if filtered_words:
    top_word, top_count = Counter(filtered_words).most_common(1)[0]

    st.subheader("📢 Most Trending Word")
    st.markdown(f"**{top_word}** (mentioned {top_count}×)")

if scored_news:
    all_text = " ".join([item["summary"].lower() for item in scored_news])
    keyword_counts = {kw: all_text.count(kw.lower()) for kw in KEYWORDS}

    # Sortiert nach Häufigkeit
    sorted_counts = dict(sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True))
    st.markdown(f"🕒 _Published: {item['timestamp']}_")
    st.subheader("📚 Keyword Occurrence Table")
    st.table(sorted_counts)

# Nach Score sortieren (höchste Relevanz oben)
scored_news.sort(key=lambda x: x["score"], reverse=True)
# Top 3 wichtigste News extrahieren
top_news = scored_news[:3]
st.subheader("🔥 Most Relevant News")
min_length = st.slider("🔤 Minimum Summary Length", min_value=50, max_value=500, value=150)

for item in scored_news:
    st.markdown(f"### {item['title']} ({item['score']}%)")
    st.write(item["summary"])
    st.markdown(f"[Read more]({item['link']})")
    st.markdown("---")

st.subheader("🏆 Top 3 Most Relevant News")

for idx, item in enumerate(top_news, start=1):
    color = score_color(item["score"])
    st.markdown(f"### {idx}. <span style='color:{color}'>{item['title']} ({item['score']}%)</span>", unsafe_allow_html=True)
    st.write(item["summary"])
    st.markdown(f"[Read full article here]({item['link']})")
    st.markdown("---")

if scored_news:
    filtered_text = " ".join([item["summary"] for item in scored_news])

    st.subheader("☁️ WordCloud of Selected Topics News")

    wordcloud = WordCloud(
        width=800, height=400, background_color='white', collocations=False
    ).generate(filtered_text)

    fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
    ax_wc.imshow(wordcloud, interpolation='bilinear')
    ax_wc.axis('off')

    st.pyplot(fig_wc)
    
if st.checkbox("🧾 Show raw data (JSON preview)"):
    st.subheader("🛠 Raw News Data")
    st.json(scored_news)

for item in news:
    if len(item["summary"]) >= min_length:
        score = relevance_score(item["summary"])
        if score >= score_threshold:
            item["score"] = score
            scored_news.append(item)
