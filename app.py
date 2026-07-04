from flask import Flask, render_template, request
from src.news_fetcher import fetch_news
from src.processor import split_texts
from src.vector_store import create_db, search
from src.summarizer import summarize

app = Flask(__name__)

vector_db = None

@app.route("/", methods=["GET", "POST"])
def home():
    global vector_db
    summary = None
    results = []

    if request.method == "POST":
        query = request.form.get("query")

        # Fetch news
        articles = fetch_news(query)

        # convert to text for vector DB
        texts = [article["title"] for article in articles]

        chunks = split_texts(texts)

        vector_db = create_db(chunks)

        docs = search(vector_db, query)

        results = articles  # for UI

        summary = summarize(docs)

    return render_template("index.html", results=results, summary=summary)


if __name__ == "__main__":
    app.run()