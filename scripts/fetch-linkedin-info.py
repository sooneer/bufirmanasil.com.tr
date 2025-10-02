#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Firma Bilgisi Çekme Script
LinkedIn linklerinden firma adı ve hakkında bilgisini çeker.
"""

import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

# Windows terminal için encoding ayarı
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def fetch_linkedin_html(linkedin_url, timeout=30):
    """LinkedIn sayfasından HTML içeriğini çeker"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }

        # SSL uyarısını bastır
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        session = requests.Session()
        session.headers.update(headers)

        response = session.get(linkedin_url, timeout=timeout, allow_redirects=True, verify=False)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            return response.text
        else:
            print(f"⚠️  HTTP {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"❌ LinkedIn HTML çekme hatası: {e}")
        return None


def clean_linkedin_text(text):
    """LinkedIn'den gelen metni temizler"""
    import html
    if not text:
        return ''

    # HTML entity'leri decode et
    text = html.unescape(text)

    # "Company Name | LinkedIn'de 123" formatını temizle
    if ' | LinkedIn' in text:
        # LinkedIn prefix'i kaldır
        parts = text.split(' | ')
        # İlk part firma bilgisi, son part LinkedIn meta
        if len(parts) >= 2:
            # "Company Name" kısmını al
            text = parts[0].strip()

    return text.strip()


def extract_linkedin_info(html):
    """HTML'den LinkedIn firma bilgilerini çıkarır"""
    soup = BeautifulSoup(html, 'html.parser')

    info = {
        'name': '',
        'about': '',
        'tagline': '',
        'industry': '',
        'company_size': '',
        'headquarters': '',
        'founded': ''
    }

    try:
        # Firma adı - meta tag'den
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            # "Company Name | LinkedIn" formatından sadece firma adını al
            title = og_title.get('content', '')
            info['name'] = clean_linkedin_text(title.split('|')[0])

        # Alternatif: title tag'den
        if not info['name']:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.text
                info['name'] = clean_linkedin_text(title.split('|')[0])

        # Hakkında (about) bilgisi - meta description'dan
        og_description = soup.find('meta', property='og:description')
        if og_description and og_description.get('content'):
            raw_about = og_description.get('content', '').strip()
            raw_about = clean_linkedin_text(raw_about)

            # LinkedIn meta formatını temizle
            # Format: "Company Name | LinkedIn'de 123 takipçi Actual description here"
            # veya: "LinkedIn'de 123 takipçi Actual description here"

            # "LinkedIn'de X takipçi/followers" kısmını kaldır
            raw_about = re.sub(r"^.*?\s*\|\s*LinkedIn'de\s+[\d\.,]+\s+takipçi\s+", '', raw_about)
            raw_about = re.sub(r"^.*?\s*\|\s*LinkedIn'de\s+[\d\.,]+\s+followers?\s+", '', raw_about)
            raw_about = re.sub(r"^LinkedIn'de\s+[\d\.,]+\s+takipçi\s+", '', raw_about)
            raw_about = re.sub(r"^LinkedIn'de\s+[\d\.,]+\s+followers?\s+", '', raw_about)

            info['about'] = raw_about.strip()

        # Alternatif: meta description tag'den
        if not info['about']:
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                raw_desc = meta_desc.get('content', '').strip()
                raw_desc = clean_linkedin_text(raw_desc)
                raw_desc = re.sub(r"^.*?\s*\|\s*LinkedIn'de\s+[\d\.,]+\s+takipçi\s+", '', raw_desc)
                raw_desc = re.sub(r"^LinkedIn'de\s+[\d\.,]+\s+takipçi\s+", '', raw_desc)
                info['about'] = raw_desc.strip()

        # Tagline - about'tan ilk anlamlı cümleyi çıkar
        if info['about'] and len(info['about']) > 20:
            # İlk cümleyi veya ilk pipe'a kadar olan kısmı al
            if '|' in info['about']:
                tagline = info['about'].split('|')[0].strip()
            else:
                # İlk cümleyi al (. veya ! veya ?)
                sentences = re.split(r'[.!?]\s+', info['about'])
                tagline = sentences[0].strip() if sentences else ''

            # Makul bir tagline uzunluğu kontrolü
            if 10 < len(tagline) < 200:
                info['tagline'] = tagline

        # JSON-LD structured data'dan bilgi çek
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    if data.get('@type') == 'Organization':
                        if not info['name'] and data.get('name'):
                            info['name'] = data['name']
                        if not info['about'] and data.get('description'):
                            info['about'] = data['description']
            except:
                continue

        # Sayfa içeriğinden detaylı bilgi çekme (JavaScript render gerektirmeden)
        # LinkedIn'in public görünümünde bazı bilgiler meta tag'lerde olabilir

        # Industry bilgisi
        for text in soup.stripped_strings:
            if 'Industry' in text or 'Sektör' in text:
                # Sonraki text node'u industry olabilir
                pass

        # Company size
        for text in soup.stripped_strings:
            if 'employees' in text.lower() or 'çalışan' in text.lower():
                # Size bilgisi
                match = re.search(r'(\d+[\-,]\d+|\d+\+?)\s*(employees|çalışan)', text, re.IGNORECASE)
                if match:
                    info['company_size'] = match.group(1)

    except Exception as e:
        print(f"⚠️  Bilgi çıkarma hatası: {e}")

    return info


def update_company_json_with_linkedin(json_path, linkedin_info, dry_run=False, force=False):
    """JSON dosyasını LinkedIn bilgileriyle günceller"""
    try:
        # JSON dosyasını oku
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Mevcut değerleri sakla
        old_name = data.get('name', '')
        old_about = data.get('about', '')
        old_tagline = data.get('tagline', '')

        updated = False
        updates = []

        # Name güncelle (sadece boşsa veya force modundaysa)
        if linkedin_info['name'] and (not old_name or force):
            data['name'] = linkedin_info['name']
            updated = True
            updates.append(f"Name: {linkedin_info['name']}")

        # About güncelle (sadece boşsa veya force modundaysa)
        if linkedin_info['about'] and (not old_about or force):
            data['about'] = linkedin_info['about']
            updated = True
            updates.append(f"About: {linkedin_info['about'][:100]}...")

        # Tagline güncelle (sadece boşsa veya force modundaysa)
        if linkedin_info['tagline'] and (not old_tagline or force):
            data['tagline'] = linkedin_info['tagline']
            updated = True
            updates.append(f"Tagline: {linkedin_info['tagline']}")

        if not updated:
            print("  ℹ️  Güncellenecek yeni bilgi bulunamadı (zaten dolu veya LinkedIn'den bilgi alınamadı)")
            return False

        # Güncellemeleri göster
        print("\n📝 Güncellenecek alanlar:")
        for update in updates:
            print(f"  • {update}")

        # Dosyayı kaydet
        if not dry_run:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n✅ Dosya güncellendi: {json_path}")
        else:
            print(f"\n🔍 DRY RUN: Dosya güncellenmedi (--dry-run)")

        return True

    except Exception as e:
        print(f"❌ JSON güncelleme hatası: {e}")
        return False


def process_single_file(json_path, args):
    """Tek bir JSON dosyasını işler"""
    print(f"\n{'='*70}")
    print(f"📂 Dosya: {json_path.name}")
    print(f"{'='*70}")

    # JSON dosyasını oku
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ JSON okuma hatası: {e}")
        return False

    # LinkedIn linkini al
    linkedin_url = data.get('social', {}).get('linkedin', '')
    if not linkedin_url:
        print("⚠️  LinkedIn linki bulunamadı")
        return False

    print(f"🔗 LinkedIn: {linkedin_url}")

    # Mevcut bilgileri göster
    print(f"\n📊 Mevcut Bilgiler:")
    print(f"  Name: {data.get('name', '(boş)')}")
    print(f"  Tagline: {data.get('tagline', '(boş)')}")
    print(f"  About: {data.get('about', '(boş)')[:100]}{'...' if len(data.get('about', '')) > 100 else ''}")

    # LinkedIn'den bilgi çek
    print(f"\n🔍 LinkedIn bilgileri çekiliyor...")
    html = fetch_linkedin_html(linkedin_url, timeout=args.timeout)

    if not html:
        print("❌ LinkedIn HTML çekilemedi")
        return False

    # Bilgileri çıkar
    linkedin_info = extract_linkedin_info(html)

    print(f"\n✅ LinkedIn'den çekilen bilgiler:")
    print(f"  Name: {linkedin_info['name'] or '(bulunamadı)'}")
    print(f"  Tagline: {linkedin_info['tagline'] or '(bulunamadı)'}")
    print(f"  About: {linkedin_info['about'][:100] if linkedin_info['about'] else '(bulunamadı)'}{'...' if len(linkedin_info['about']) > 100 else ''}")

    # JSON'u güncelle
    success = update_company_json_with_linkedin(json_path, linkedin_info, dry_run=args.dry_run, force=args.force)

    return success


def process_all_files(args):
    """Tüm company JSON dosyalarını işler"""
    company_dir = Path('public/data/company')

    if not company_dir.exists():
        print(f"❌ Klasör bulunamadı: {company_dir}")
        return

    # Tüm JSON dosyalarını al
    json_files = sorted(company_dir.glob('*.json'))

    if not json_files:
        print(f"❌ JSON dosyası bulunamadı: {company_dir}")
        return

    print(f"📁 Toplam {len(json_files)} dosya bulundu")

    if args.limit:
        json_files = json_files[:args.limit]
        print(f"⚠️  Limit uygulandı: İlk {args.limit} dosya işlenecek")

    # İstatistikler
    stats = {
        'total': len(json_files),
        'success': 0,
        'failed': 0,
        'skipped': 0
    }

    # Her dosyayı işle
    for i, json_path in enumerate(json_files, 1):
        print(f"\n{'='*70}")
        print(f"[{i}/{len(json_files)}] İşleniyor...")
        print(f"{'='*70}")

        try:
            success = process_single_file(json_path, args)
            if success:
                stats['success'] += 1
            else:
                stats['skipped'] += 1
        except Exception as e:
            print(f"❌ Hata: {e}")
            stats['failed'] += 1

        # Rate limiting - LinkedIn'in throttle yapmaması için
        if i < len(json_files):
            wait_time = args.delay
            print(f"\n⏳ {wait_time} saniye bekleniyor...")
            time.sleep(wait_time)

    # Özet
    print(f"\n{'='*70}")
    print(f"📊 İŞLEM ÖZETİ")
    print(f"{'='*70}")
    print(f"Toplam: {stats['total']}")
    print(f"Başarılı: {stats['success']}")
    print(f"Atlandı: {stats['skipped']}")
    print(f"Hatalı: {stats['failed']}")
    print(f"{'='*70}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn firma bilgilerini çeker ve JSON dosyalarını günceller')
    parser.add_argument('json_file', nargs='?', help='İşlenecek JSON dosyası (belirtilmezse tüm dosyalar işlenir)')
    parser.add_argument('--all', action='store_true', help='Tüm company JSON dosyalarını işle')
    parser.add_argument('--limit', type=int, help='İşlenecek maksimum dosya sayısı')
    parser.add_argument('--dry-run', action='store_true', help='Sadece göster, dosyayı güncelleme')
    parser.add_argument('--force', action='store_true', help='Mevcut bilgilerin üzerine yaz')
    parser.add_argument('--timeout', type=int, default=30, help='HTTP timeout (saniye, varsayılan: 30)')
    parser.add_argument('--delay', type=int, default=5, help='Dosyalar arası bekleme süresi (saniye, varsayılan: 5)')

    args = parser.parse_args()

    # Tüm dosyaları işle
    if args.all or not args.json_file:
        process_all_files(args)
        return 0

    # Tek dosya işle
    json_path = Path(args.json_file)
    if not json_path.exists():
        # public/data/company/ içinde ara
        alt_path = Path('public/data/company') / json_path.name
        if alt_path.exists():
            json_path = alt_path
        else:
            print(f"❌ Dosya bulunamadı: {args.json_file}")
            return 1

    success = process_single_file(json_path, args)
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
