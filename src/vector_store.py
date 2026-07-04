from types import SimpleNamespace

def create_db(chunks):
    """
    Store chunks in memory.
    """
    return chunks


def search(db, query, k=5):
    """
    Rank chunks by simple keyword overlap.
    Returns objects with .page_content just like LangChain Documents.
    """

    query_words = set(query.lower().split())

    scored = []

    for chunk in db:
        chunk_words = set(chunk.lower().split())
        score = len(query_words & chunk_words)
        scored.append((score, chunk))

    scored.sort(reverse=True)

    results = [
        SimpleNamespace(page_content=text)
        for score, text in scored[:k]
    ]

    return results