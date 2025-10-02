# LinkedIn Selenium Script Kullanım Kılavuzu

## 🎯 Özellikler
- Selenium ile tarayıcı otomasyonu
- Giriş yapmış tarayıcı oturumunu kullanma
- Detaylı firma bilgilerini çekme (about, tagline, industry, company size, vb.)

## 📋 Kullanım Örnekleri

### 1. Basit Kullanım (Yeni tarayıcı oturumu)
```bash
python scripts/fetch-linkedin-info-selenium.py public/data/company/akgun.json
```

### 2. Opera Profilinizi Kullanarak (GİRİŞ YAPMIŞ OTURUM)
```bash
# Opera profil yolu genellikle:
# C:\Users\{KULLANICI_ADI}\AppData\Roaming\Opera Software\Opera Stable

python scripts/fetch-linkedin-info-selenium.py public/data/company/akgun.json --profile "C:\Users\{KULLANICI_ADI}\AppData\Roaming\Opera Software\Opera Stable"
```

### 3. Chrome Profilinizi Kullanarak
```bash
# Chrome profil yolu:
# C:\Users\{KULLANICI_ADI}\AppData\Local\Google\Chrome\User Data

python scripts/fetch-linkedin-info-selenium.py public/data/company/akgun.json --profile "C:\Users\{KULLANICI_ADI}\AppData\Local\Google\Chrome\User Data"
```

### 4. Tüm Firmalar İçin (İlk 5 firma ile test)
```bash
python scripts/fetch-linkedin-info-selenium.py --all --limit 5 --profile "C:\Users\{KULLANICI_ADI}\AppData\Roaming\Opera Software\Opera Stable"
```

### 5. Tüm Firmalar (Profil ile)
```bash
python scripts/fetch-linkedin-info-selenium.py --all --delay 10 --profile "C:\Users\{KULLANICI_ADI}\AppData\Roaming\Opera Software\Opera Stable"
```

## 🔧 Parametreler

- `json_file`: İşlenecek JSON dosyası (opsiyonel)
- `--all`: Tüm company dosyalarını işle
- `--limit N`: Maksimum N dosya işle
- `--dry-run`: Değişiklikleri kaydetme, sadece göster
- `--force`: Mevcut bilgilerin üzerine yaz
- `--timeout N`: Sayfa yükleme timeout (varsayılan: 30)
- `--delay N`: Dosyalar arası bekleme (varsayılan: 5)
- `--profile PATH`: Tarayıcı profil dizini (giriş yapmış oturum için)

## 📝 Önemli Notlar

1. **Profil Kullanımı**: Profil kullanırken tüm Opera/Chrome pencerelerini kapatın
2. **Manuel Giriş**: Eğer login wall'a yönlendirilirseniz, manuel giriş yapabilirsiniz
3. **Rate Limiting**: LinkedIn'in throttle yapmaması için delay kullanın (10+ saniye önerilir)
4. **Tarayıcı Görünür**: Script çalışırken tarayıcı penceresi açılacak (headless değil)

## 🔍 Opera Profil Yolunu Bulma

Windows PowerShell'de:
```powershell
ls "$env:APPDATA\Opera Software\Opera Stable"
```

## 💡 İpuçları

- İlk çalıştırmada `--limit 1` ile test edin
- Büyük toplu işlemler için `--delay 10` veya daha fazla kullanın
- Eğer "authwall" hatası alırsanız, manuel giriş yapmanız istenecek
