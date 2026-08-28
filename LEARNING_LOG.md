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
### Gün 3 - Docker, Git ve CI/CD

**Docker**
- Image vs container farkını öğrendim: image = kalıp/tarif, container = 
  o kalıbın çalışan hali
- Katman (layer) mantığı: Docker her satırı cache'liyor, bu yüzden az 
  değişen şeyleri (requirements.txt) üstte, sık değişenleri (kod) altta 
  tutmak build hızını artırıyor
- .dockerignore ile venv/, chroma_db/, .env gibi şeyleri image'a 
  kopyalamaktan kaçındım
- Volume kavramı: chroma_db'yi image içine gömmek yerine, container 
  dışındaki gerçek diske "bağladım" (-v ile) - böylece container silinse 
  bile veri kaybolmuyor
- API key'i image'a gömmek yerine --env-file ile dışarıdan verdim (güvenlik)
- Gözlem: container içinde embedding modeli sıfırdan indirildi çünkü 
  container, benim yerel cache'ime erişemiyor - ileride optimize edilebilir 
  bir nokta (modeli build sırasında image'a gömmek gibi)
- Gözlem: çok kısa/belirsiz sorularda (örn. tek kelime "agent") LLM 
  bazen tutarsız/farklı dilde cevap verebiliyor - prompt engineering ile 
  iyileştirilebilir bir alan

**Git & GitHub**
- git init, add, commit, push akışını ilk kez uçtan uca deneyimledim
- "Gömülü repo" hatası: data/temp_langchain_docs kendi içinde bir git 
  reposu olduğu için ana projeye submodule gibi eklenmeye çalışıldı - 
  .gitignore'a ekleyip git rm -r --cached -f ile temizledim
- .gitignore sayesinde .env, venv/, chroma_db/ gibi hassas/gereksiz 
  dosyalar GitHub'a hiç gitmedi

**GitHub Actions (CI/CD)**
- .github/workflows/ klasöründeki YAML dosyalarının otomatik çalıştığını 
  öğrendim
- İlk pipeline'ım: her push'ta kodu çekip, Python kurup, dependencies 
  kurup, basit bir import testi yapıyor
- İlk çalıştırmada başarılı sonuç aldım (succeeded, tüm adımlar yeşil)

### Gün 4 - LLMOps: Loglama

- generate_answer() fonksiyonuna time, datetime, json modülleriyle 
  loglama ekledim - her istekte soru, cevap, chunk_sayisi, sure_saniye, 
  zaman bilgilerini logs.jsonl dosyasına kaydediyorum
- .jsonl formatı: her satır bağımsız bir JSON objesi, "a" (append) 
  modunda dosyaya ekleniyor - normal JSON dosyasından farkı bu
- time.time() ile başlangıç/bitiş zamanını alıp farkını hesaplayarak 
  işlem süresini ölçmeyi öğrendim

**Beklenmedik ama öğretici bir sorun: Model deprecation**
- llama-3.3-70b-versatile modeli çalışırken aniden 404 hatası vermeye 
  başladı: "model does not exist or you do not have access to it"
- Araştırınca öğrendim ki Groq, bu modeli gerçekten kullanımdan 
  kaldırmış (Ağustos 2026 itibarıyla) - benim hatam değilmiş
- openai/gpt-oss-120b modeline geçince sorun çözüldü
- Bu, gerçek production sistemlerinde sürekli karşılaşılan bir durum: 
  dış API sağlayıcıları modelleri değiştirebiliyor/kaldırabiliyor, 
  sistemin buna karşı esnek olması gerekiyor (örneğin model adını 
  hardcode etmek yerine config'den okumak gibi bir iyileştirme 
  düşünülebilir)
- Gözlem: aynı soruya ("agent") arka arkaya sorduğumda LLM farklı 
  cevaplar üretti - modellerin deterministik olmadığını bizzat gördüm

## Gün 4 (devam) - LLMOps: Token/Maliyet Takibi ve Prompt Versiyonlama

**Token/Maliyet Takibi**
- response.usage nesnesinin prompt_tokens, completion_tokens, total_tokens 
  bilgilerini içerdiğini öğrendim
- Groq ücretsiz olduğu için gerçek maliyet yok, ama OpenAI'ın gpt-4o-mini 
  fiyatlandırmasına göre "bu sorgu OpenAI'da olsaydı ne kadar tutardı" 
  şeklinde simüle bir maliyet hesapladım
- Hata: log_recs dictionary'sini oluşturdum ama dosyaya yazan kodu 
  silmişim, "oluşturup unutmak" gibi bir hata yaptım - fonksiyonun 
  return ettiği şeyle, içeride oluşturduğun ama kullanmadığın değişkenler 
  farklı şeyler, ikisini karıştırmışım

**Prompt Versiyonlama**
- Prompt'u kod içine gömmek yerine ayrı bir prompts.py dosyasında, 
  versiyon numarasıyla (CURRENT_VERSION) sözlük olarak tuttum
- str.format() metodunu öğrendim - f-string'e benzer ama string önceden 
  tanımlıysa (fonksiyon dışında) kullanılıyor
- Her log kaydına hangi prompt versiyonunun kullanıldığını da ekledim - 
  ileride prompt'u değiştirirsem, hangi versiyonun nasıl performans 
  gösterdiğini karşılaştırabilirim

**Genel gözlem:** Bugün RAG'ın "temel çalışması" ile "gerçek bir ürün 
gibi izlenebilir/yönetilebilir olması" arasındaki farkı deneyimledim - 
loglama, maliyet takibi, versiyonlama gibi şeyler kodun çalışmasını 
değiştirmiyor ama sistemi çok daha "profesyonel" ve sürdürülebilir 
yapıyor.