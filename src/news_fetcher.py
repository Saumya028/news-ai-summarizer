import feedparser
from urllib.parse import quote

def fetch_news(topic="ai"):
    encoded_topic = quote(topic)   # ✅ FIX

    url = f"https://news.google.com/rss/search?q={encoded_topic}"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:5]:
        articles.append(entry.title + ". " + entry.summary)

    return articles