def split_texts(texts, chunk_size=500, overlap=50):
    chunks = []

    step = chunk_size - overlap

    for text in texts:
        start = 0

        while start < len(text):
            chunks.append(text[start:start + chunk_size])
            start += step

    return chunks