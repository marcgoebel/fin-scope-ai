# news/news_scraper.py
import feedparser
from datetime import datetime

def get_finance_news(feed_url="https://www.handelsblatt.com/contentexport/feed/finanzen"):
    feed = feedparser.parse(feed_url)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return [
        {
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "timestamp": now  # ⏰ hinzufügen!
        }
        for entry in feed.entries
    ]