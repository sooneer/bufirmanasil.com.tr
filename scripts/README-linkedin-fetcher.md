# LinkedIn URL Fetcher

Bu script, `linkedin-links-list.txt` dosyasındaki tüm LinkedIn URL'lerine istek gönderir ve sonuçları otomatik olarak kaydeder.

## Kullanım

### Temel Kullanım
```bash
npm run fetch-linkedin
```

veya doğrudan:
```bash
node scripts/fetch-linkedin-pages.js
```

## Özellikler

- ✅ Tüm URL'leri otomatik olarak okur
- ✅ Her URL'ye sırayla istek atar
- ✅ Sonuçları ayrı TXT dosyalarına kaydeder
- ✅ İstekler arası bekleme süresi (rate limiting)
- ✅ Timeout kontrolü
- ✅ Hata yönetimi
- ✅ İlerleme takibi
- ✅ Özet rapor

## Çıktılar

### Dosya Konumu
Tüm sonuçlar `linkedin-responses/` klasörüne kaydedilir.

### Dosya Adlandırma
Her URL için şirket adına göre dosya oluşturulur:
- `https://www.linkedin.com/company/komtas-bilgi-yonetimi` → `komtas-bilgi-yonetimi.txt`

### Dosya İçeriği
```
URL: https://www.linkedin.com/company/...
Tarih: 2025-10-01T12:00:00.000Z
Status: 200

=== HEADERS ===
{
  "content-type": "text/html",
  ...
}

=== BODY ===
<!DOCTYPE html>
...
```

## Konfigürasyon

Script içinde `CONFIG` nesnesini düzenleyerek ayarları değiştirebilirsiniz:

```javascript
const CONFIG = {
  inputFile: 'linkedin-links-list.txt',  // Kaynak dosya
  outputDir: 'linkedin-responses',        // Çıktı klasörü
  delay: 3000,                            // İstekler arası bekleme (ms)
  timeout: 30000,                         // Request timeout (ms)
  userAgent: '...'                        // User-Agent header
};
```

## Notlar

- Script her istek arasında 3 saniye bekler (LinkedIn rate limiting için)
- Hata durumlarında da dosya oluşturulur
- İlerleme console'da gösterilir
- Tüm işlem bittiğinde özet rapor gösterilir

## Örnekler

### Başarılı İşlem
```
[1/368] İşleniyor: https://www.linkedin.com/company/komtas-bilgi-yonetimi
  ✓ Kaydedildi: komtas-bilgi-yonetimi.txt (Status: 200)
  Bekleniyor... (3s)
```

### Hatalı İşlem
```
[2/368] İşleniyor: https://www.linkedin.com/company/invalid-company
  ✗ Hata: Request timeout
```

### İşlem Özeti
```
==================================================
İşlem tamamlandı!
Başarılı: 350
Başarısız: 18
Toplam: 368
Sonuçlar: linkedin-responses
==================================================
```
