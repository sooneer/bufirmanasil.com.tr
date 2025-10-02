# LinkedIn Remote Debugging Kullanım Kılavuzu

## 🎯 Adım 1: Opera'yı Remote Debugging ile Başlat

### PowerShell'de çalıştır:

```powershell
# Opera'yı kapat
taskkill /F /IM opera.exe

# Remote debugging ile başlat
Start-Process "C:\Users\soner.acar\AppData\Local\Programs\Opera\opera.exe" -ArgumentList "--remote-debugging-port=9222"
```

VEYA doğrudan Opera kısayoluna sağ tık > Özellikler > Hedef kısmına ekle:
```
--remote-debugging-port=9222
```

## 🎯 Adım 2: LinkedIn'e Giriş Yap

Opera'da `linkedin.com` adresine gidin ve hesabınızla giriş yapın.

## 🎯 Adım 3: Scripti Çalıştır

### Test (Tek firma):
```powershell
python scripts/fetch-linkedin-info-remote.py public/data/company/akgun.json
```

### İlk 5 firma:
```powershell
python scripts/fetch-linkedin-info-remote.py --all --limit 5 --delay 10
```

### Tüm firmalar:
```powershell
python scripts/fetch-linkedin-info-remote.py --all --delay 10
```

## ✅ Kontrol

Script çalıştığında Opera'da otomatik olarak LinkedIn sayfaları açılacak ve bilgiler çekilecek.

## 🔧 Sorun Giderme

### "Tarayıcıya bağlanırken hata"
- Opera'nın `--remote-debugging-port=9222` ile başlatıldığından emin olun
- Opera'da `chrome://version` adresine gidip "Command Line" satırında `--remote-debugging-port=9222` olduğunu kontrol edin

### "LinkedIn giriş ekranına yönlendirildi"
- Opera'da LinkedIn'e giriş yapın
- Scripti tekrar çalıştırın

## 📊 Çekilecek Bilgiler

✅ Firma Adı (name)
✅ Hakkında (about) 
✅ Tagline/Slogan
✅ Sektör (industry)
✅ Çalışan Sayısı (company size)
✅ Genel Merkez (headquarters)
✅ Kuruluş Yılı (founded)
✅ Website
