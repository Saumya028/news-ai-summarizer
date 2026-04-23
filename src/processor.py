from langchain_text_splitters import CharacterTextSplitter

def split_texts(texts):
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = []
    for text in texts:
        chunks.extend(splitter.split_text(text))

    return chunks