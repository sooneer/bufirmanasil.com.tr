# LinkedIn URL Fetcher - Kullanım Kılavuzu

## 🚫 CORS Sorunu Nedir?

CORS (Cross-Origin Resource Sharing), tarayıcıların güvenlik mekanizmasıdır. LinkedIn gibi siteler, tarayıcıdan direkt JavaScript ile erişimi engellemektedir.

## ✅ Çözümler

### 1. Node.js ile Backend Script (ÖNERİLEN) ⭐

CORS sorunu olmaz, en güvenilir yöntemdir.

```powershell
# Terminal'de çalıştırın
npm run fetch-linkedin
```

veya

```powershell
node scripts/fetch-linkedin-pages.js
```

**Avantajları:**
- ✅ CORS sorunu yok
- ✅ Hızlı ve güvenilir
- ✅ Rate limit problemi yok
- ✅ Tüm URL'leri işleyebilir

**Çıktı:**
- Sonuçlar `linkedin-responses/` klasörüne kaydedilir
- Her URL için ayrı `.txt` dosyası oluşturulur

### 2. Tarayıcı + CORS Proxy (Alternatif)

Tarayıcıda çalışır ama proxy servisi gerektirir.

```powershell
# HTML dosyasını açın
start scripts/fetch-linkedin-proxy.html
```

**Proxy Seçenekleri:**
1. **AllOrigins** (Önerilen): Güvenilir ama yavaş olabilir
2. **CORS Proxy**: Hızlı ama rate limit var
3. **Özel Proxy**: Kendi proxy sunucunuz

**Dikkat:**
- ⚠️ Proxy servisleri yavaş olabilir
- ⚠️ Rate limit sorunları yaşanabilir
- ⚠️ Bazı proxy'ler LinkedIn'i engelleyebilir

### 3. Selenium ile Tarama (Mevcut Python Script)

Gerçek tarayıcı kullanarak veri çeker.

```powershell
python scripts/fetch-linkedin-info-selenium.py --all --delay 8 --timeout 30
```

**Avantajları:**
- ✅ JavaScript render edilmiş içerik
- ✅ LinkedIn giriş yapabilme
- ✅ Tam sayfa içeriği

**Dezavantajları:**
- ❌ Yavaş
- ❌ Chrome/Firefox gerektirir
- ❌ Sistem kaynağı tüketir

## 📊 Karşılaştırma

| Yöntem | Hız | CORS | Güvenilirlik | Kullanım |
|--------|-----|------|--------------|----------|
| **Node.js** | ⚡⚡⚡ | ✅ | ⭐⭐⭐⭐⭐ | Terminal |
| **Proxy + Tarayıcı** | ⚡⚡ | ⚠️ | ⭐⭐⭐ | HTML |
| **Selenium** | ⚡ | ✅ | ⭐⭐⭐⭐ | Terminal |

## 🎯 Önerilen Kullanım

### Küçük Test (10 URL)
```powershell
node scripts/fetch-linkedin-pages.js
# veya config'de limit ayarlayın
```

### Tüm URL'ler (352 URL)
```powershell
# Tahmini süre: 352 × 3 saniye = ~18 dakika
npm run fetch-linkedin
```

### Sonuçları İnceleme
```powershell
# Kaydedilen dosyaları listele
ls linkedin-responses/

# Bir dosyayı oku
cat linkedin-responses/komtas-bilgi-yonetimi.txt
```

## ⚙️ Ayarlar (Node.js)

`scripts/fetch-linkedin-pages.js` dosyasındaki `CONFIG` nesnesini düzenleyin:

```javascript
const CONFIG = {
  inputFile: 'linkedin-links-list.txt',  // Kaynak dosya
  outputDir: 'linkedin-responses',        // Çıktı klasörü
  delay: 3000,                            // İstekler arası bekleme (ms)
  timeout: 30000,                         // Request timeout (ms)
  userAgent: '...'                        // User-Agent header
};
```

## 🛠️ Sorun Giderme

### "npm run fetch-linkedin" çalışmıyor
```powershell
# Doğrudan çalıştırın
node scripts/fetch-linkedin-pages.js
```

### Timeout Hataları
```javascript
// CONFIG'de timeout'u artırın
timeout: 60000  // 60 saniye
```

### Rate Limiting
```javascript
// İstekler arası beklemeyi artırın
delay: 5000  // 5 saniye
```

### LinkedIn Bloklama
- User-Agent değiştirin
- Delay süresini artırın
- Selenium kullanın

## 📝 Sonuç Formatı

Her URL için oluşturulan dosya formatı:

```
URL: https://www.linkedin.com/company/komtas-bilgi-yonetimi
Tarih: 2025-10-01T12:00:00.000Z
Status: 200

=== HEADERS ===
{
  "content-type": "text/html",
  "content-length": "123456"
}

=== BODY ===
<!DOCTYPE html>
<html>...
```

## 🚀 Hızlı Başlangıç

1. **Node.js yüklü mü kontrol edin:**
   ```powershell
   node --version
   ```

2. **Script'i çalıştırın:**
   ```powershell
   npm run fetch-linkedin
   ```

3. **Sonuçları kontrol edin:**
   ```powershell
   ls linkedin-responses/
   ```

İşte bu kadar! 🎉
