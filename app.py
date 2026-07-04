from flask import Flask, render_template, request
from src.news_fetcher import fetch_news
from src.summarizer import summarize

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    summary = None
    results = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if query:
            # Fetch news articles
            articles = fetch_news(query)

            results = articles

            # Prepare text for AI summarization
            texts = []

            for article in articles:
                article_text = f"""
Title: {article.get('title', '')}
Source: {article.get('source', '')}
Date: {article.get('published', '')}
Summary: {article.get('summary', '')[:300]}
Link: {article.get('link', '')}
"""
                texts.append(article_text)

            # Generate AI summary only if articles were found
            if texts:
                summary = summarize(texts)
            else:
                summary = "No news articles found for this topic."

    return render_template(
        "index.html",
        results=results,
        summary=summary
    )


if __name__ == "__main__":
    app.run(debug=True)