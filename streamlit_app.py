# streamlit_app.py

import streamlit as st
from news.news_scraper import get_finance_news

st.set_page_config(page_title="FinScope AI", layout="wide")
st.title("🧠 FinScope AI – Smart Finance News Filter")

st.markdown("This app fetches the latest financial news and prepares it for AI-based filtering. 🚀")

# News anzeigen
news = get_finance_news()

st.subheader("📰 Latest Headlines")
for item in news:
    st.markdown(f"### [{item['title']}]({item['link']})")
    st.write(item["summary"])
    st.markdown("---")
