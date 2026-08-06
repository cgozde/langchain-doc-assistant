#yol = "data/temp_langchain_docs/src/oss/langchain/quickstart.mdx"
#with open(yol, "r") as dosya:
#    icerik = dosya.read()
 #   print(icerik[:200])  # ilk 200 karakteri yazdır
def load_documents():
    dosyalar = ["quickstart.mdx", "overview.mdx", "install.mdx", "agents.mdx", "models.mdx", 
    "tools.mdx", "messages.mdx", "retrieval.mdx", "structured-output.mdx", 
    "streaming.mdx", "short-term-memory.mdx", "long-term-memory.mdx", 
    "human-in-the-loop.mdx", "mcp.mdx", "context-engineering.mdx"]
    dokumanlar = []
    for eleman in dosyalar:
        dosya_path = (f"data/temp_langchain_docs/src/oss/langchain/{eleman}")
        with open(dosya_path, "r") as dosya:
            icerik = dosya.read()
            belge = {"dosya_adi": dosya_path, "icerik": icerik}
        dokumanlar.append(belge)
    return dokumanlar
            
