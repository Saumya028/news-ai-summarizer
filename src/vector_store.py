from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_db(chunks):
    return FAISS.from_texts(chunks, embedding_model)

def search(db, query):
    return db.similarity_search(query, k=5)  # improved