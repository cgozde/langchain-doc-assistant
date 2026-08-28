# LangChain Doc Assistant

LangChain dokümantasyonu üzerinde çalışan bir RAG (Retrieval-Augmented Generation) tabanlı soru-cevap asistanı. Kullanıcı bir soru sorar, sistem LangChain'in resmi dokümantasyonundan en alakalı bölümleri bulur ve bu bilgiye dayanarak bir LLM ile cevap üretir.

## Özellikler

- LangChain dokümantasyonundan otomatik veri çekme ve işleme
- Semantik arama (embedding tabanlı retrieval)
- Groq API (Llama/GPT-OSS modelleri) ile hızlı, ücretsiz cevap üretimi
- FastAPI ile REST API servisi
- Docker ile containerization
- GitHub Actions ile otomatik test (CI)
- Loglama: her isteğin süresi, token kullanımı, tahmini maliyeti kaydediliyor
- Prompt versiyonlama

## Mimari

Kullanıcı Sorusu
│
▼
FastAPI (/ask endpoint)
│
▼
Retrieval (Chroma vector DB'den en alakalı 3 chunk bulunur)
│
▼
Generation (chunk'lar + soru, Groq LLM'e gönderilir)
│
▼
Cevap + Loglama (logs.jsonl)


## Kullanılan Teknolojiler

- **Python 3.9**
- **LangChain** — dokümantasyon işleme
- **ChromaDB** — vector veritabanı
- **sentence-transformers** — embedding (all-MiniLM-L6-v2)
- **Groq API** — LLM inference (openai/gpt-oss-120b)
- **FastAPI** — REST API
- **Docker** — containerization
- **GitHub Actions** — CI/CD

## Kurulum

### Yerel (venv ile)

\`\`\`bash
git clone https://github.com/cgozde/langchain-doc-assistant.git
cd langchain-doc-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env dosyası oluştur, içine Groq API key'ini ekle:
echo "GROQ_API_KEY=your_key_here" > .env

uvicorn src.api.main:app --reload
\`\`\`

### Docker ile

\`\`\`bash
docker build -t langchain-doc-assistant .
docker run -p 8000:8000 --env-file .env -v $(pwd)/chroma_db:/app/chroma_db langchain-doc-assistant
\`\`\`

## Kullanım

Sunucu çalıştıktan sonra:

\`\`\`
GET http://localhost:8000/ask?soru=How do I create an agent?
\`\`\`

**Örnek cevap:**
\`\`\`json
{
  "cevap": "To create an agent in LangChain, you can use the create_agent function..."
}
\`\`\`

İnteraktif dokümantasyon için: `http://localhost:8000/docs`

## Proje Yapısı

\`\`\`
├── src/
│   ├── api/              # FastAPI endpoint'leri
│   ├── generation/      # LLM ile cevap üretme, prompt yönetimi
│   ├── ingestion/      # Doküman yükleme ve chunking 
│   └── retrieval/      # Embedding ve arama
├── Dockerfile
├── .github/workflows/    # CI pipeline
└── requirements.txt
\`\`\`

## Öğrenme Süreci

Bu proje, RAG sistemlerini ve MLOps/LLMOps pratiklerini uçtan uca öğrenmek amacıyla geliştirildi. Süreç boyunca tutulan detaylı notlar için [LEARNING_LOG.md](./LEARNING_LOG.md) dosyasına bakabilirsiniz.