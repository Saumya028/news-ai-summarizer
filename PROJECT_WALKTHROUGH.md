# 📰 AI News Summarizer - Complete Project Walkthrough

## 🎯 Project Overview

**AI News Summarizer** is a Flask-based web application that fetches news articles on a given topic, processes them using AI embeddings, and generates intelligent summaries using LLMs (Large Language Models).

**Technology Stack:**
- **Backend:** Flask (Python web framework)
- **NLP Processing:** LangChain
- **Vector Database:** FAISS (Facebook AI Similarity Search)
- **Embeddings:** HuggingFace Sentence Transformers
- **LLM:** OpenRouter API with Llama-3-8B
- **News Source:** Google RSS Feed
- **Frontend:** Jinja2 HTML Templates

---

## 🏗️ Architecture Overview

```
User Input (Query)
      ↓
    [1] Fetch News Articles (Google RSS)
      ↓
    [2] Split into Chunks (Text Processing)
      ↓
    [3] Create Vector Database (FAISS)
      ↓
    [4] Semantic Search (Find Relevant Chunks)
      ↓
    [5] AI Summarization (LLM)
      ↓
    Display Results + Summary
```

---

## 📁 Project Structure

```
news-ai-summarizer/
├── app.py                    # Main Flask application & routes
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation (currently empty)
│
├── src/                      # Core module files
│   ├── news_fetcher.py       # Fetches articles from Google RSS
│   ├── processor.py          # Splits text into chunks
│   ├── summarizer.py         # Generates summaries using LLM
│   └── vector_store.py       # Creates & searches vector database
│
└── templates/
    └── index.html            # Web UI template
```

---

## 🔄 Complete Data Flow Walkthrough

### **Step 1: User Interaction**
- User visits Flask app homepage (`http://localhost:5000`)
- Sees HTML form with text input field for topic query
- Submits query via POST request (e.g., "AI startups")

### **Step 2: News Fetching** (`news_fetcher.py`)
```python
def fetch_news(topic="ai"):
    encoded_topic = quote(topic)  # URL-encode the query
    url = f"https://news.google.com/rss/search?q={encoded_topic}"
    feed = feedparser.parse(url)
    # Returns top 5 articles as list
```
- **Input:** User's search query (e.g., "AI startups")
- **Process:** 
  - Constructs Google News RSS feed URL
  - Parses RSS feed using `feedparser`
  - Extracts article title + summary
- **Output:** List of 5 articles (text format)

### **Step 3: Text Processing** (`processor.py`)
```python
def split_texts(texts):
    splitter = CharacterTextSplitter(
        chunk_size=500,       # Each chunk = ~500 characters
        chunk_overlap=50      # 50 char overlap between chunks
    )
    chunks = []
    for text in texts:
        chunks.extend(splitter.split_text(text))
    return chunks
```
- **Input:** List of 5 articles
- **Process:**
  - Splits each article into manageable 500-character chunks
  - Maintains 50-character overlap (for context continuity)
  - Prevents context loss at chunk boundaries
- **Output:** List of ~10-15 chunks (depends on article length)

### **Step 4: Vector Database Creation** (`vector_store.py`)
```python
def create_db(chunks):
    embedding_model = HuggingFaceEmbeddings()
    return FAISS.from_texts(chunks, embedding_model)
```
- **Input:** Text chunks
- **Process:**
  - Converts each chunk to vector embedding using HuggingFace model
  - Each embedding = 384-dimensional vector (semantic representation)
  - Stores vectors in FAISS index for fast similarity search
- **Output:** FAISS vector database object

### **Step 5: Semantic Search** (`vector_store.py`)
```python
def search(db, query):
    return db.similarity_search(query, k=3)
```
- **Input:** Vector DB + user query
- **Process:**
  - Converts query to embedding (same model as chunks)
  - Finds 3 most similar chunks using cosine similarity
  - Returns most relevant articles
- **Output:** 3 most relevant document chunks

### **Step 6: AI Summarization** (`summarizer.py`)
```python
def summarize(docs):
    text = "\n\n".join([d.page_content for d in docs])
    prompt = """Summarize the following news:
    [text]
    Give: Key Points, Trends, Final Summary"""
    response = llm.invoke(prompt)
    return response.content
```
- **Input:** 3 relevant document chunks
- **Process:**
  - Combines chunks into single text
  - Sends to Llama-3-8B LLM via OpenRouter API
  - LLM generates structured summary with:
    - Key Points
    - Trends
    - Final Summary
- **Output:** AI-generated summary (text)

### **Step 7: Display Results** (Flask + Jinja2)
- Renders `index.html` with:
  - Search form (for new queries)
  - List of 3 relevant articles
  - AI-generated summary

---

## 💻 Main Application Flow (`app.py`)

```python
@app.route("/", methods=["GET", "POST"])
def home():
    global vector_db
    summary = None
    results = []

    if request.method == "POST":
        query = request.form.get("query")           # Step 1: Get user input
        articles = fetch_news(query)                # Step 2: Fetch news
        chunks = split_texts(articles)              # Step 3: Process texts
        vector_db = create_db(chunks)               # Step 4: Create DB
        docs = search(vector_db, query)             # Step 5: Search
        results = [d.page_content for d in docs]    # Step 6: Extract results
        summary = summarize(docs)                   # Step 7: Summarize

    return render_template("index.html", results=results, summary=summary)
```

---

## 🚀 How to Run

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Set API Key**
⚠️ **IMPORTANT:** The `summarizer.py` already contains an OpenRouter API key for testing. For production:
- Get your own key from https://openrouter.ai
- Replace the key in `src/summarizer.py`

### **3. Run Flask App**
```bash
python app.py
```

### **4. Access Application**
- Open browser → `http://localhost:5000`
- Enter search topic (e.g., "AI startups", "Climate change")
- Click "Search"
- View articles + AI summary

---

## 🔑 Key Technologies Explained

| Component | Purpose |
|-----------|---------|
| **feedparser** | Parses RSS/Atom feeds from Google News |
| **LangChain** | Simplifies LLM & vector DB interactions |
| **FAISS** | Fast similarity search on embeddings |
| **HuggingFace** | Pre-trained sentence embedding model |
| **OpenRouter** | API gateway for various LLMs |
| **Llama-3-8B** | Open-source LLM for summarization |

---

## 📊 Example User Journey

**User Input:** "Machine Learning breakthroughs 2024"

**Process:**
1. Fetches 5 latest ML news articles from Google
2. Splits into ~12 chunks (each ~500 chars)
3. Creates vector embeddings for semantic understanding
4. Finds 3 most relevant chunks to the query
5. Sends those chunks to Llama-3-8B LLM
6. LLM returns:
   ```
   Key Points:
   - New transformer architecture improves efficiency
   - Vision models show superhuman performance
   
   Trends:
   - Multimodal models gaining adoption
   - Smaller efficient models competing with large ones
   
   Final Summary:
   Recent ML breakthroughs focus on efficiency and multimodal capabilities...
   ```

---

## ⚙️ Configuration & Tuning

### **Text Processing** (`processor.py`)
- `chunk_size=500` → Increase for longer context
- `chunk_overlap=50` → Increase to prevent context loss

### **Search** (`vector_store.py`)
- `k=3` → Return top 3 results. Change to get more/fewer articles

### **Summarization** (`summarizer.py`)
- `temperature=0.3` → Lower = more focused, Higher = more creative
- Model choice → Can swap `meta-llama/llama-3-8b-instruct` for other models

### **News Source** (`news_fetcher.py`)
- `[:5]` → Gets top 5 articles. Can increase for more articles

---

## 🔒 Security Notes

⚠️ **Current Issues:**
1. OpenRouter API key is exposed in `summarizer.py`
   - **Solution:** Use environment variables
   ```python
   import os
   OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
   ```

2. No error handling for API failures
   - **Solution:** Add try-catch blocks for API calls

---

## 🎓 Learning Points

**This project demonstrates:**
1. **LLM Integration** → Using OpenRouter API with LangChain
2. **Vector Databases** → FAISS for semantic search
3. **Text Processing** → Chunking and embedding text
4. **Web Frameworks** → Flask routing and templating
5. **RSS Parsing** → Fetching news from feeds
6. **RAG Architecture** → Retrieval-Augmented Generation pattern

---

## ✅ Quick Reference

| What | Where | Function |
|------|-------|----------|
| **Web Routes** | `app.py` | Flask app setup & routes |
| **News Source** | `src/news_fetcher.py` | Google News RSS fetching |
| **Text Chunking** | `src/processor.py` | Split articles into chunks |
| **Vector DB** | `src/vector_store.py` | FAISS embeddings & search |
| **Summarization** | `src/summarizer.py` | LLM-based summary generation |
| **UI** | `templates/index.html` | Web interface |

---

## 🚦 Next Steps / Enhancements

1. **Add error handling** for API failures
2. **Hide API keys** using environment variables
3. **Cache results** to avoid repeated API calls
4. **Add source links** to news articles
5. **User authentication** for personalized summaries
6. **Multiple language support** for international news
7. **Better UI/CSS styling** for professional look
8. **Async processing** for faster performance
9. **Multiple LLM options** user can choose from
10. **Sentiment analysis** on summarized articles
