#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn response dosyalarini parse edip company JSON dosyalarina ekler
"""

import os
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import argparse
import requests
from urllib.parse import urlparse
import time

# Output encoding fix for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Dizinler
LINKEDIN_RESPONSES_DIR = Path("linkedin-responses")
COMPANY_DATA_DIR = Path("public/data/company")
LOGO_DIR = Path("public/img/company")

def extract_linkedin_info(html_content):
    """HTML iceriginden LinkedIn bilgilerini cikarir"""
    info = {
        "companyName": None,
        "tagline": None,
        "description": None,
        "website": None,
        "industry": None,
        "companySize": None,
        "headquarters": None,
        "specialties": None,
        "followers": None,
        "logoUrl": None
    }

    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Sirket adi - meta tag'den
        name_meta = soup.find('meta', {'property': 'og:title'})
        if name_meta:
            info['companyName'] = name_meta.get('content', '').strip()

        # Logo URL - og:image meta tag'den
        logo_meta = soup.find('meta', {'property': 'og:image'})
        if logo_meta:
            logo_url = logo_meta.get('content', '').strip()
            if logo_url and 'company-logo' in logo_url:
                info['logoUrl'] = logo_url

        # Tagline - h4 tag'inden (top-card-layout__second-subline)
        tagline_tag = soup.find('h4', {'class': re.compile(r'top-card-layout__second-subline')})
        if tagline_tag:
            tagline_span = tagline_tag.find('span')
            if tagline_span:
                tagline = tagline_span.get_text().strip()
                # HTML entities'leri temizle
                tagline = tagline.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                if tagline and len(tagline) > 5:
                    info['tagline'] = tagline

        # Takipci sayisi - meta description'dan
        desc_meta = soup.find('meta', {'property': 'og:description'})
        if desc_meta:
            desc = desc_meta.get('content', '').strip()
            # Takipci sayisini ayir
            follower_match = re.search(r'(\d+(?:[.,]\d+)?[KMB]?)\s+takipci', desc, re.IGNORECASE)
            if follower_match:
                info['followers'] = follower_match.group(1)

        # About/Hakkinda bolumu - JSON-LD'den veya text'ten
        scripts = soup.find_all('script', {'type': 'application/ld+json'})
        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    if 'description' in data:
                        info['description'] = data['description']
                    if 'name' in data and not info['companyName']:
                        info['companyName'] = data['name']
            except:
                pass

        # Diger bilgiler - text iceriginden
        text = soup.get_text()

        # Web sitesi
        website_match = re.search(r'Web\s*sitesi[:\s]+([^\s]+)', text, re.IGNORECASE)
        if website_match:
            info['website'] = website_match.group(1).strip()

        # Sektor/Industry - HTML yapisindan
        # Oncelikle h2 tag'inden (top-card-layout__headline)
        industry_tag = soup.find('h2', {'class': re.compile(r'top-card-layout__headline')})
        if industry_tag:
            industry_text = industry_tag.get_text().strip()
            if industry_text and len(industry_text) > 5 and len(industry_text) < 200:
                info['industry'] = industry_text

        # Yoksa text'ten regex ile bul
        if not info['industry']:
            industry_match = re.search(r'Sektor[:\s]+([^\n]+)', text, re.IGNORECASE)
            if not industry_match:
                industry_match = re.search(r'Industry[:\s]+([^\n]+)', text, re.IGNORECASE)
            if industry_match:
                industry_text = industry_match.group(1).strip()
                if industry_text and len(industry_text) > 5 and len(industry_text) < 200:
                    info['industry'] = industry_text

        # Sirket buyuklugu
        size_match = re.search(r'Sirket buyuklugu[:\s]+([^\n]+)', text, re.IGNORECASE)
        if not size_match:
            size_match = re.search(r'Company size[:\s]+([^\n]+)', text, re.IGNORECASE)
        if size_match:
            info['companySize'] = size_match.group(1).strip()

        # Genel merkez
        hq_match = re.search(r'Genel merkez[:\s]+([^\n]+)', text, re.IGNORECASE)
        if not hq_match:
            hq_match = re.search(r'Headquarters[:\s]+([^\n]+)', text, re.IGNORECASE)
        if hq_match:
            info['headquarters'] = hq_match.group(1).strip()

        # Uzmanliklar
        spec_match = re.search(r'Uzmanliklar[:\s]+([^\n]+)', text, re.IGNORECASE)
        if not spec_match:
            spec_match = re.search(r'Specialties[:\s]+([^\n]+)', text, re.IGNORECASE)
        if spec_match:
            info['specialties'] = spec_match.group(1).strip()

    except Exception as e:
        print(f"  [!] Parse hatasi: {e}")

    return info

def find_company_json_by_linkedin(linkedin_url):
    """LinkedIn URL'sine gore company JSON dosyasini bulur"""
    if not linkedin_url:
        return None

    # LinkedIn URL'den slug cikar
    linkedin_slug = linkedin_url.replace('https://linkedin.com/company/', '')
    linkedin_slug = linkedin_slug.replace('https://www.linkedin.com/company/', '')
    linkedin_slug = linkedin_slug.replace('/', '').replace('?', '').strip()

    # Tum company JSON dosyalarini tara
    for json_file in COMPANY_DATA_DIR.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            company_linkedin = data.get('social', {}).get('linkedin', '')
            if not company_linkedin:
                continue

            # LinkedIn URL'lerini karsilastir
            company_slug = company_linkedin.replace('https://linkedin.com/company/', '')
            company_slug = company_slug.replace('https://www.linkedin.com/company/', '')
            company_slug = company_slug.replace('/', '').replace('?', '').strip()

            if company_slug.lower() == linkedin_slug.lower():
                return json_file

        except Exception as e:
            continue

    return None

def update_company_json(json_file, linkedin_info):
    """Company JSON dosyasini LinkedIn bilgileriyle gunceller"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        updated = False

        # Name guncelle - "| LinkedIn" ifadesini kaldir
        if linkedin_info['companyName']:
            clean_name = linkedin_info['companyName'].replace(' | LinkedIn', '').strip()
            current_name = data.get('name', '')
            # Sadece bos ise veya LinkedIn'den gelen isim farkli ise guncelle
            if not current_name or current_name == '':
                data['name'] = clean_name
                updated = True

        # Tagline guncelle - LinkedIn'den gelen veri daha guncel ve kaliteli
        if linkedin_info['tagline']:
            current_tagline = data.get('tagline', '')
            if linkedin_info['tagline'] != current_tagline:
                data['tagline'] = linkedin_info['tagline']
                updated = True

        # About guncelle - LinkedIn'den gelen description uzunsa ve farkli ise guncelle
        if linkedin_info['description']:
            current_about = data.get('about', '')
            # LinkedIn'den gelen description daha uzun veya mevcut about cok kisaysa guncelle
            if (len(linkedin_info['description']) > len(current_about) or
                len(current_about) < 50 or
                linkedin_info['description'] != current_about):
                data['about'] = linkedin_info['description']
                updated = True

        # Industry'yi sector dizisine ekle (sadece anlamli ise)
        if linkedin_info['industry'] and len(linkedin_info['industry']) > 5 and len(linkedin_info['industry']) < 200:
            if 'sector' not in data:
                data['sector'] = []
            # Eger sector bos veya yok ise ekle
            if not data['sector'] or len(data['sector']) == 0:
                data['sector'] = [linkedin_info['industry']]
                updated = True
            # Eger sector var ama bu industry yoksa ekle
            elif linkedin_info['industry'] not in data['sector']:
                data['sector'].append(linkedin_info['industry'])
                updated = True

        # Company size'i en disariya ekle
        if linkedin_info['companySize'] and not data.get('companySize'):
            data['companySize'] = linkedin_info['companySize']
            updated = True

        # Headquarters'i en disariya ekle
        if linkedin_info['headquarters'] and not data.get('headquarters'):
            data['headquarters'] = linkedin_info['headquarters']
            updated = True

        # Website'i contact'a ekle
        if linkedin_info['website'] and not data.get('contact', {}).get('web'):
            if 'contact' not in data:
                data['contact'] = {}
            if not data['contact'].get('web'):
                data['contact']['web'] = linkedin_info['website']
                updated = True

        # Logo indir ve guncelle
        if linkedin_info['logoUrl']:
            # Slug'i al - dosya adini kullan
            company_slug = Path(json_file).stem

            # Logo'yu indir
            logo_path = download_logo(linkedin_info['logoUrl'], company_slug)

            # Basarili ise JSON'u guncelle
            if logo_path:
                current_logo = data.get('logo', '')
                if current_logo != logo_path:
                    data['logo'] = logo_path
                    updated = True

        # Eski linkedinInfo alanini kaldir (artik gereksiz)
        if 'linkedinInfo' in data:
            del data['linkedinInfo']
            updated = True

        if updated:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True

        return False

    except Exception as e:
        print(f"  [X] JSON guncelleme hatasi: {e}")
        return False

def download_logo(logo_url, company_slug, max_retries=3):
    """LinkedIn'den logo indirir ve yerel dosyaya kaydeder

    Args:
        logo_url: LinkedIn logo URL
        company_slug: Sirket slug (dosya adi icin)
        max_retries: Maksimum deneme sayisi

    Returns:
        str: Logo dosya yolu (ornek: 'img/company/4thewall.png') veya None
    """
    if not logo_url or not company_slug:
        return None

    # Logo dizinini olustur
    LOGO_DIR.mkdir(parents=True, exist_ok=True)

    # Dosya uzantisini belirle
    ext = 'png'
    if '.jpg' in logo_url.lower() or '.jpeg' in logo_url.lower():
        ext = 'jpg'

    logo_filename = f"{company_slug}.{ext}"
    logo_path = LOGO_DIR / logo_filename
    logo_relative_path = f"img/company/{logo_filename}"

    # Zaten varsa indirme
    if logo_path.exists():
        print(f"  [i] Logo zaten mevcut: {logo_relative_path}")
        return logo_relative_path

    # Logo'yu indir
    for attempt in range(max_retries):
        try:
            print(f"  [↓] Logo indiriliyor: {logo_url[:80]}...")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(logo_url, headers=headers, timeout=10)
            response.raise_for_status()

            # Content-type kontrolu
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"  [!] Gecersiz content-type: {content_type}")
                return None

            # Dosyayi kaydet
            with open(logo_path, 'wb') as f:
                f.write(response.content)

            print(f"  [✓] Logo indirildi: {logo_relative_path} ({len(response.content)} bytes)")
            return logo_relative_path

        except requests.exceptions.RequestException as e:
            print(f"  [!] Logo indirme hatasi (deneme {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Yeniden denemeden once bekle
            continue
        except Exception as e:
            print(f"  [X] Beklenmeyen hata: {e}")
            return None

    print(f"  [X] Logo indirilemedi: {company_slug}")
    return None

def process_linkedin_responses(limit=None, dry_run=False):
    """LinkedIn response dosyalarini isler"""

    if not LINKEDIN_RESPONSES_DIR.exists():
        print(f"[X] {LINKEDIN_RESPONSES_DIR} klasoru bulunamadi!")
        return

    if not COMPANY_DATA_DIR.exists():
        print(f"[X] {COMPANY_DATA_DIR} klasoru bulunamadi!")
        return

    response_files = sorted(LINKEDIN_RESPONSES_DIR.glob("*.txt"))

    if limit:
        response_files = response_files[:limit]

    print(f"[*] Toplam {len(response_files)} LinkedIn response dosyasi bulundu\n")

    if dry_run:
        print("[!] DRY RUN MODE - Hicbir degisiklik yapilmayacak\n")

    processed = 0
    updated = 0
    not_found = 0
    errors = 0

    for i, response_file in enumerate(response_files, 1):
        print(f"[{i}/{len(response_files)}] Isleniyor: {response_file.name}")

        try:
            # Response dosyasini oku
            with open(response_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # URL'yi cikar
            url_match = re.search(r'^URL:\s*(.+)$', content, re.MULTILINE)
            if not url_match:
                print("  [!] URL bulunamadi")
                errors += 1
                continue

            linkedin_url = url_match.group(1).strip()

            # HTML icerigini cikar
            body_match = re.search(r'=== BODY ===\s*(.+)', content, re.DOTALL)
            if not body_match:
                print("  [!] HTML icerigi bulunamadi")
                errors += 1
                continue

            html_content = body_match.group(1)

            # LinkedIn bilgilerini parse et
            linkedin_info = extract_linkedin_info(html_content)

            if linkedin_info['companyName']:
                print(f"  [+] Sirket: {linkedin_info['companyName']}")

            # Ilgili company JSON dosyasini bul
            json_file = find_company_json_by_linkedin(linkedin_url)

            if not json_file:
                print(f"  [!] JSON dosyasi bulunamadi: {linkedin_url}")
                not_found += 1
                continue

            print(f"  [OK] JSON bulundu: {json_file.name}")

            # JSON dosyasini guncelle
            if not dry_run:
                if update_company_json(json_file, linkedin_info):
                    print(f"  [OK] Guncellendi!")
                    updated += 1
                else:
                    print(f"  [-] Guncellenecek veri yok")
            else:
                print(f"  [DRY RUN] Guncelleme atlandi")

            processed += 1
            print()

        except Exception as e:
            print(f"  [X] Hata: {e}\n")
            errors += 1

    # Ozet
    print("\n" + "="*60)
    print("[*] Islem Tamamlandi!")
    print("="*60)
    print(f"[OK] Islenen:        {processed}")
    print(f"[OK] Guncellenen:    {updated}")
    print(f"[!]  Bulunamayan:    {not_found}")
    print(f"[X]  Hata:           {errors}")
    print(f"[*]  Toplam:         {len(response_files)}")
    print("="*60)

def main():
    parser = argparse.ArgumentParser(
        description='LinkedIn response dosyalarini parse edip company JSON dosyalarina ekler'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Islenecek maksimum dosya sayisi'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Degisiklik yapmadan test et'
    )

    args = parser.parse_args()

    print("="*60)
    print("LinkedIn Response Parser")
    print("="*60)
    print()

    process_linkedin_responses(limit=args.limit, dry_run=args.dry_run)

if __name__ == '__main__':
    main()
