# LinkedIn Response Parser

Bu script, `linkedin-responses/` klasöründeki LinkedIn HTML yanıtlarını parse ederek önemli bilgileri `public/data/company/` klasöründeki JSON dosyalarına ekler.

## 🎯 Ne Yapar?

LinkedIn HTML sayfalarından şu bilgileri çıkarır ve ilgili şirketin JSON dosyasına ekler:

### Çıkarılan Bilgiler

- **companyName**: Şirket adı
- **tagline**: Kısa açıklama/slogan
- **description**: Detaylı açıklama (About bölümü)
- **industry**: Sektör
- **companySize**: Şirket büyüklüğü (çalışan sayısı)
- **headquarters**: Genel merkez
- **specialties**: Uzmanlık alanları
- **followers**: Takipçi sayısı
- **website**: Web sitesi

### JSON Yapısı

Bilgiler şirket JSON dosyalarına `linkedinInfo` anahtarı altında eklenir:

```json
{
  "name": "Şirket Adı",
  "tagline": "LinkedIn'den gelen tagline (eğer boşsa)",
  "about": "LinkedIn'den gelen açıklama (eğer boş veya kısaysa)",
  "linkedinInfo": {
    "name": "Şirket Adı | LinkedIn",
    "industry": "Bilgi Teknolojileri ve Hizmetleri",
    "companySize": "51-200 çalışan",
    "headquarters": "İstanbul, Türkiye",
    "specialties": "Yazılım, Web, Mobil",
    "followers": "5.234"
  }
}
```

## 🚀 Kullanım

### Temel Kullanım

```powershell
# Tüm dosyaları işle
python scripts/parse-linkedin-responses.py
```

### Parametreler

#### --limit
İşlenecek maksimum dosya sayısı:

```powershell
# İlk 10 dosyayı işle
python scripts/parse-linkedin-responses.py --limit 10
```

#### --dry-run
Hiçbir değişiklik yapmadan test et:

```powershell
# Sadece test et, değişiklik yapma
python scripts/parse-linkedin-responses.py --dry-run

# İlk 5 dosya ile test
python scripts/parse-linkedin-responses.py --limit 5 --dry-run
```

## 📊 Çıktı Formatı

```
============================================================
LinkedIn Response Parser
============================================================

[*] Toplam 348 LinkedIn response dosyasi bulundu

[1/348] Isleniyor: 4thewall.txt
  [+] Sirket: 4THEWALL | LinkedIn
  [OK] JSON bulundu: 4thewall.json
  [OK] Guncellendi!

[2/348] Isleniyor: adesso.txt
  [+] Sirket: adesso Turkey | LinkedIn
  [OK] JSON bulundu: adesso-turkey.json
  [-] Guncellenecek veri yok

...

============================================================
[*] Islem Tamamlandi!
============================================================
[OK] Islenen:        348
[OK] Guncellenen:    234
[!]  Bulunamayan:    5
[X]  Hata:           9
[*]  Toplam:         348
============================================================
```

## 🔍 Nasıl Çalışır?

### 1. LinkedIn Response Dosyası Okuma
```
linkedin-responses/4thewall.txt
├── URL: https://www.linkedin.com/company/4thewall
├── Headers
└── HTML Body
```

### 2. HTML Parse Etme
- BeautifulSoup ile HTML ayrıştırma
- Meta tag'lerden bilgi çekme
- JSON-LD verilerini okuma
- Text içeriğinden regex ile bilgi çıkarma

### 3. JSON Dosyası Bulma
LinkedIn URL'sinden şirket slug'ı çıkarılır ve `public/data/company/` klasöründeki JSON dosyaları taranır.

### 4. JSON Güncelleme
- Sadece **boş** veya **eksik** alanlar güncellenir
- Mevcut veriler **korunur**
- `linkedinInfo` bölümü eklenir/güncellenir

## ⚙️ Gereksinimler

```powershell
pip install beautifulsoup4
```

## 📁 Dosya Yapısı

```
linkedin-responses/          # LinkedIn HTML yanıtları
│   4thewall.txt
│   adesso.txt
│   ...
│
public/data/company/         # Şirket JSON dosyaları
│   4thewall.json
│   adesso-turkey.json
│   ...
│
scripts/
│   parse-linkedin-responses.py    # Ana script
│   fetch-linkedin-pages.js        # LinkedIn'den veri çekme (Node.js)
│   ...
```

## 🎯 Kullanım Senaryoları

### Senaryo 1: İlk Kez Kullanım
```powershell
# Test için ilk 5 dosya
python scripts/parse-linkedin-responses.py --limit 5 --dry-run

# Eğer sonuç iyiyse, gerçekten güncelle
python scripts/parse-linkedin-responses.py --limit 5

# Hepsi için çalıştır
python scripts/parse-linkedin-responses.py
```

### Senaryo 2: Yeni LinkedIn Verileri Eklendi
```powershell
# Tüm dosyaları tekrar işle
# Sadece boş alanlar güncellenecek
python scripts/parse-linkedin-responses.py
```

### Senaryo 3: Hata Durumu
```powershell
# Log dosyasını kontrol et
Get-Content linkedin-parse.log | Select-String "Hata"

# Sadece belirli sayıda dosya işle
python scripts/parse-linkedin-responses.py --limit 100
```

## 🛡️ Güvenlik

- **Mevcut veriler korunur**: Script sadece boş alanları doldurur
- **Backup önerilir**: İşlem öncesi `public/data/company/` klasörünü yedekleyin
- **Dry-run kullanın**: Önce `--dry-run` ile test edin

## 📝 Örnek JSON Güncellemesi

### Önce
```json
{
  "name": "BilgeAdam",
  "tagline": "",
  "about": "BilgeAdam Teknoloji",
  "social": {
    "linkedin": "https://linkedin.com/company/bilgeadam"
  }
}
```

### Sonra
```json
{
  "name": "BilgeAdam",
  "tagline": "Teknoloji ve İnovasyon Lideri",
  "about": "BilgeAdam Teknoloji, 1990 yılından bu yana Türkiye'nin önde gelen teknoloji şirketlerinden biridir...",
  "social": {
    "linkedin": "https://linkedin.com/company/bilgeadam"
  },
  "linkedinInfo": {
    "name": "BilgeAdam Teknoloji | LinkedIn",
    "industry": "Bilgi Teknolojileri ve Hizmetleri",
    "companySize": "1.001-5.000 çalışan",
    "headquarters": "İstanbul, Türkiye",
    "specialties": "Yazılım Geliştirme, Danışmanlık, Eğitim",
    "followers": "47.891"
  }
}
```

## 🐛 Sorun Giderme

### UnicodeEncodeError
Windows terminal encoding sorunu. Script otomatik olarak UTF-8'e geçer.

### JSON Dosyası Bulunamadı
LinkedIn URL'si ile JSON dosyasındaki URL eşleşmiyor. Manuel kontrol gerekir:
```powershell
# LinkedIn URL'sini kontrol et
Get-Content linkedin-responses/sirket.txt | Select-String "URL:"

# JSON dosyasını kontrol et
Get-Content public/data/company/sirket.json | Select-String "linkedin"
```

### BeautifulSoup Kurulu Değil
```powershell
pip install beautifulsoup4
```

## 🔗 İlgili Scriptler

- **fetch-linkedin-pages.js**: LinkedIn sayfalarını çeker ve `linkedin-responses/` klasörüne kaydeder
- **fetch-linkedin-proxy.html**: Tarayıcı tabanlı alternatif
- **LINKEDIN-FETCHER-GUIDE.md**: Detaylı kullanım kılavuzu

## 📊 İstatistikler

Script çalıştırıldığında:
- İşlenen dosya sayısı
- Güncellenen dosya sayısı
- Bulunamayan JSON dosyası sayısı
- Hata sayısı

rapor edilir.

---

**Not**: Bu script LinkedIn'den çekilen HTML yanıtlarını parse eder. LinkedIn sayfalarını çekmek için önce `fetch-linkedin-pages.js` veya `fetch-linkedin-proxy.html` kullanılmalıdır.
