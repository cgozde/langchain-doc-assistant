## Gün 1 - Doküman Yükleme
- Python'da open()/with ile dosya okumayı öğrendim
- 15 LangChain dokümanını dictionary listesi olarak yükleyen bir script yazdım
- Zorluk: LangChain repo yapısı beklediğimden farklıydı, docs klasörü değişmiş - google/github arayarak doğru yolu buldum
- Doküman içeriğinde Mintlify'a özel :::python :::js işaretleri var, chunking aşamasında temizlemem gerekebilir
### Neden Chunking?
- tüm sayfayı veya bağlamı LLM'e göndermek zordur bu yüzden parçalar halinde gönderiyoruz
- alakalı parçaları gönderdiğimizde daha isabetli sonuçlar elde edebiliyoruz
- Overlap (parçalar arası örtüşme) kullandık, çünkü kesin sınırlarla bölersek bir cümle/fikir ortadan kesilebilir, bağlam kaybolur
- chunk_size=1000, overlap=200 ile başladık - bu değerler ileride performansa göre ayarlanabilir bir hyperparameter
- Fonksiyonu başka dosyada tekrar kullanmak için (chunk_docs.py'da) load_docs.py'ı import ettik - kod tekrar kullanılabilirliği önemli
### Retrieval
- - Retrieval çalışıyor, agent sorgusu doğru chunk'ları buluyor
- Ama bazı chunk'lar Mintlify import satırları gibi "gürültü" içeriyor 
- ileride chunking öncesi temizlik (preprocessing) eklemek gerekebilir
### Gün 2 - Generation (RAG'ı Tamamlama)
- Groq API ile LLM'e bağlanmayı öğrendim, Claude API ile Pro aboneliğinin 
  ayrı şeyler olduğunu fark ettim (Pro = chat arayüzü, API = ayrı ücretli erişim)
- retrieval'den gelen chunk'ları context olarak birleştirip, soruyla birlikte 
  LLM'e prompt olarak gönderdim
- Önemli hata: Python kodu yukarıdan aşağıya çalışıyor, bir değişkeni 
  (prompt) kullanılacağı satırdan SONRA tanımlarsam NameError alıyorum - 
  sıralama önemli
- Sonuç: RAG sistemi artık uçtan uca çalışıyor - soru soruyorum, 
  Chroma'dan alakalı LangChain dokümantasyonu bulunuyor, Groq bu bilgiye 
  dayanarak doğru cevap üretiyor
- Sıradaki adım: bunu FastAPI ile servis haline getirmek