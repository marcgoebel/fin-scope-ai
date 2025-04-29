# streamlit_app.py

import streamlit as st
from news.news_scraper import get_finance_news
from ai.relevance_filter import is_relevant
from ai.relevance_filter import relevance_score
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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
    
# Nach Score sortieren (höchste Relevanz oben)
scored_news.sort(key=lambda x: x["score"], reverse=True)
# Top 3 wichtigste News extrahieren
top_news = scored_news[:3]
st.subheader("🔥 Most Relevant News")

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
