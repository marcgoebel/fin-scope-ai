# streamlit_app.py

import streamlit as st
from news.news_scraper import get_finance_news
from ai.relevance_filter import is_relevant
from ai.relevance_filter import relevance_score
import pandas as pd


st.set_page_config(page_title="FinScope AI", layout="wide")
st.title("🧠 FinScope AI – Smart Finance News Filter")
score_threshold = st.slider("🎯 Minimum Relevance Score", min_value=0, max_value=100, value=30)
st.markdown("This app fetches the latest financial news and prepares it for AI-based filtering. 🚀")

# News anzeigen
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

# Nach Score sortieren (höchste Relevanz oben)
scored_news.sort(key=lambda x: x["score"], reverse=True)
st.subheader("🔥 Most Relevant News")

for item in scored_news:
    st.markdown(f"### {item['title']} ({item['score']}%)")
    st.write(item["summary"])
    st.markdown(f"[Read more]({item['link']})")
    st.markdown("---")
