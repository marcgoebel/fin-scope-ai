# streamlit_app.py

import streamlit as st
from news.news_scraper import get_finance_news
from ai.relevance_filter import is_relevant
from ai.relevance_filter import relevance_score

st.set_page_config(page_title="FinScope AI", layout="wide")
st.title("🧠 FinScope AI – Smart Finance News Filter")

st.markdown("This app fetches the latest financial news and prepares it for AI-based filtering. 🚀")

# News anzeigen
news = get_finance_news()
filtered_news = [item for item in news if is_relevant(item["summary"])]

# Scored News
scored_news = []
for item in news:
    score = relevance_score(item["summary"])
    if score > 0:
        item["score"] = score
        scored_news.append(item)

# Nach Score sortieren (höchste Relevanz oben)
scored_news.sort(key=lambda x: x["score"], reverse=True)
st.subheader("📰 Latest Headlines")
for item in filtered_news:
    st.markdown(f"### [{item['title']}]({item['link']})")
    st.write(item["summary"])
    st.markdown("---")
