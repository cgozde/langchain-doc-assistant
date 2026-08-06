import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ingestion"))

from chunk_docs import get_all_chunks
from sentence_transformers import SentenceTransformer
import chromadb

all_chunks = get_all_chunks()
id_list = []
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="langchain_docs")
for index, eleman in enumerate(all_chunks):
    id_list.append(f"chunk_{index}")

collection.add(
    documents=all_chunks,
    ids=id_list
)
print(collection.count())
