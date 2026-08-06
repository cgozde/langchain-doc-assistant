import chromadb

def get_relevant_chunks(soru, n=3):
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="langchain_docs")
    sonuclar = collection.query(
        query_texts=[soru],
        n_results=n
    )
    return sonuclar["documents"][0]
