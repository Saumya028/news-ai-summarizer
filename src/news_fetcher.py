import feedparser
from urllib.parse import quote
import re


def clean_html(text):
    return re.sub('<.*?>', '', text)


def fetch_news(topic="ai"):
    encoded_topic = quote(topic + " latest news India")
    url = f"https://news.google.com/rss/search?q={encoded_topic}"
    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:5]:
        articles.append({
            "title": clean_html(entry.title),
            "link": entry.link,
            "source": entry.source.title if "source" in entry else "Unknown",

            # NEW
            "published": entry.get("published", "Not Available"),

            # NEW
            "summary": clean_html(entry.get("summary", "No summary available"))
        })

    return articles