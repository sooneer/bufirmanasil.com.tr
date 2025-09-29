# Sosyal Medya Linki Güncelleme Script'leri

Bu script'ler şirket web sitelerinden sosyal medya linklerini otomatik olarak çeker ve JSON dosyalarını günceller.

## Gereksinimler

```bash
pip install -r requirements.txt
```

veya

```bash
C:/Github/sooneer/bufirmanasil.com.tr/.venv/Scripts/python.exe -m pip install -r scripts/requirements.txt
```

## Kullanım

### Tek Şirket İçin

```bash
# Dry run (sadece göster, güncelleme)
python scripts/update-social-links.py public/data/company/innova.json --dry-run

# Gerçek güncelleme
python scripts/update-social-links.py public/data/company/innova.json

# SSL doğrulaması ile
python scripts/update-social-links.py public/data/company/innova.json --verify-ssl

# Timeout ayarı
python scripts/update-social-links.py public/data/company/innova.json --timeout 15
```

### Toplu Güncelleme

```bash
# Tüm şirketler için dry run
python scripts/batch-update-social-links.py --dry-run

# Tüm şirketleri güncelle (5 paralel işlem)
python scripts/batch-update-social-links.py

# 10 paralel işlem ile
python scripts/batch-update-social-links.py --workers 10

# Sadece belirli şirketler (regex ile)
python scripts/batch-update-social-links.py --filter "innova|softtech|logo"

# Timeout ayarı ile
python scripts/batch-update-social-links.py --timeout 15
```

## Özellikler

### Desteklenen Sosyal Medya Platformları

- ✅ LinkedIn (company ve personal profiller)
- ✅ Twitter/X
- ✅ Instagram
- ✅ Facebook
- ✅ YouTube (channel, user, @ formatları)
- ✅ GitHub

### Akıllı Link Çıkarma

- Web sitesindeki tüm linkler taranır
- Sosyal medya platformları için regex pattern matching
- Relative URL'ler otomatik absolute yapılır
- Temiz, standart format URL'ler üretilir

### Güvenli Güncelleme

- Sadece boş sosyal medya alanları doldurulur
- Mevcut değerler korunur (overwrite edilmez)
- UTF-8 encoding ile Türkçe karakter desteği
- JSON formatı korunur (indentation)
- Dry-run modu ile önce test

### SSL Desteği

- Default olarak SSL doğrulaması kapalı (bazı TR sitelerde sorun olmaması için)
- `--verify-ssl` ile açılabilir

## Örnek Çıktı

```
📂 Dosya: public\data\company\innova.json
🌐 Web Sitesi: https://innova.com.tr

🔍 Sosyal medya linkleri aranıyor...

✅ Facebook: https://facebook.com/innovabilisim
✅ Linkedin: https://linkedin.com/company/innova
✅ Youtube: https://youtube.com/@InnovaTr
✅ X: https://x.com/innovabilisim
✅ Instagram: https://instagram.com/innova_bilisim

📊 Toplam 5 sosyal medya linki bulundu

📝 JSON dosyası güncelleniyor...

  📝 linkedin güncellendi: https://linkedin.com/company/innova
  📝 x güncellendi: https://x.com/innovabilisim
  📝 instagram güncellendi: https://instagram.com/innova_bilisim
  📝 facebook güncellendi: https://facebook.com/innovabilisim
  📝 youtube güncellendi: https://youtube.com/@InnovaTr
✅ Dosya güncellendi: public\data\company\innova.json
```

## Kısıtlamalar

- JavaScript ile render edilen dinamik içerik desteklenmez (Selenium gerekir)
- Bazı siteler bot koruması kullanabilir
- Rate limiting için toplu işlemlerde paralel işlem sayısını sınırlayın
- SSL sertifikası olmayan/hatalı sitelerde sorun olabilir (default olarak ignore edilir)

## Sorun Giderme

### SSL Hatası
```bash
# --verify-ssl bayrağını KALDIRIN (default olarak kapalı)
python scripts/update-social-links.py public/data/company/akgun.json
```

### Timeout
```bash
# Timeout süresini artırın
python scripts/update-social-links.py public/data/company/akgun.json --timeout 30
```

### Link Bulunamadı
- Web sitesi JavaScript ile render ediyor olabilir
- Sosyal medya linkleri footer/header'da değil, başka bir sayfada olabilir
- Link formatı standart olmayabilir (pattern'e uymayabilir)

## İpuçları

1. **İlk önce dry-run yapın**: `--dry-run` ile test edin
2. **Filtreleme kullanın**: Önce birkaç şirket ile test edin
3. **Paralel işlem**: Çok fazla paralel işlem rate limiting'e sebep olabilir
4. **Manuel kontrol**: Script'in bulamadığı linkleri manuel ekleyin

## Gelecek İyileştirmeler

- [ ] Selenium ile JavaScript destekli siteler
- [ ] Daha fazla sosyal medya platformu (TikTok, Medium, vb.)
- [ ] Logo indirme özelliği
- [ ] Email scraping
- [ ] Telefon numarası çıkarma
- [ ] Adres bilgisi çıkarma
