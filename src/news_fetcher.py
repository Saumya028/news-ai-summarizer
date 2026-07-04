import feedparser
from urllib.parse import quote
from datetime import datetime, timezone
import re


def clean_html(text):
    return re.sub("<.*?>", "", text).strip()


def fetch_news(topic="ai"):
    encoded_topic = quote(f"{topic} latest news India")
    url = f"https://news.google.com/rss/search?q={encoded_topic}"

    feed = feedparser.parse(url)

    articles = []
    seen_titles = set()

    # Split query into keywords
    query_words = set(topic.lower().split())

    for entry in feed.entries[:20]:

        title = clean_html(entry.title)

        # Remove exact duplicate titles
        normalized_title = title.lower()

        if normalized_title in seen_titles:
            continue

        seen_titles.add(normalized_title)

        # Filter by publication date (last 3 days)
        try:
            published_dt = datetime(
                *entry.published_parsed[:6],
                tzinfo=timezone.utc
            )

            days_old = (datetime.now(timezone.utc) - published_dt).days

            if days_old > 30:
                continue

            published = published_dt.strftime("%d %b %Y %H:%M UTC")

        except Exception:
            published = "Unknown"

        summary = clean_html(
            entry.get("summary", "No summary available")
        )

        # Relevance score based on title + summary
        title_words = set(title.lower().split())
        summary_words = set(summary.lower().split())

        score = (
            len(query_words & title_words) * 3
            + len(query_words & summary_words)
        )

        articles.append({
            "title": title,
            "link": entry.link,
            "source": entry.source.title if "source" in entry else "Unknown",
            "published": published,
            "summary": summary,
            "score": score
        })

    # Sort by relevance score
    articles.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Return top 5
    return articles[:5]