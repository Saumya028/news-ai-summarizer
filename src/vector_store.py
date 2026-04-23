from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = HuggingFaceEmbeddings()

def create_db(chunks):
    return FAISS.from_texts(chunks, embedding_model)

def search(db, query):
    return db.similarity_search(query, k=3)