from load_docs import load_documents
def split_into_chunks(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while (start < len(text)):
        part= text[start:(start+chunk_size)]
        chunks.append(part)
        start = (start + chunk_size) - overlap
    return chunks

def get_all_chunks():
    dokumanlar = load_documents()
    tum_chunklar = []
    for belge in dokumanlar:
        parcalar = split_into_chunks(belge["icerik"])
        for parca in parcalar:
            tum_chunklar.append(parca)
    return tum_chunklar