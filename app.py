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

        # Step 1: Fetch news
        articles = fetch_news(query)

        # Step 2: Process
        chunks = split_texts(articles)

        # Step 3: Vector DB
        vector_db = create_db(chunks)

        # Step 4: Search
        docs = search(vector_db, query)

        results = [d.page_content for d in docs]

        # Step 5: Summarize
        summary = summarize(docs)

    return render_template("index.html", results=results, summary=summary)


if __name__ == "__main__":
    app.run(debug=True)