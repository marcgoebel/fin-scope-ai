# news/news_scraper.py
import feedparser

def get_finance_news(feed_url="https://www.handelsblatt.com/contentexport/feed/finanzen"):
    feed = feedparser.parse(feed_url)
    return [
        {"title": entry.title, "link": entry.link, "summary": entry.summary}
        for entry in feed.entries
    ]
