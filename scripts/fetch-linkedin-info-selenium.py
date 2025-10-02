#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Firma Bilgisi Çekme Script (Selenium ile)
Tarayıcı oturumu kullanarak LinkedIn'den firma bilgilerini çeker.
"""

import json
import re
import sys
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Windows terminal için encoding ayarı
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def create_driver(use_existing_profile=False, profile_path=None, headless=False):
    """Selenium WebDriver oluşturur"""
    options = Options()

    if use_existing_profile and profile_path:
        # Mevcut tarayıcı profilini kullan
        options.add_argument(f"user-data-dir={profile_path}")

    # Diğer ayarlar
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Headless mode
    if headless:
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    try:
        # WebDriver Manager ile otomatik driver yükleme
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Selenium detection'ı bypass et
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"❌ WebDriver oluşturma hatası: {e}")
        print("💡 Chrome WebDriver'ı yüklemeniz gerekebilir:")
        print("   pip install selenium")
        print("   pip install webdriver-manager")
        return None
def fetch_linkedin_with_selenium(driver, linkedin_url, timeout=30, skip_on_auth=True):
    """Selenium ile LinkedIn sayfasını çeker"""
    try:
        driver.get(linkedin_url)

        # Sayfanın yüklenmesini bekle
        time.sleep(3)

        # Login wall kontrolü
        if "authwall" in driver.current_url or "login" in driver.current_url:
            if skip_on_auth:
                print("⚠️  LinkedIn giriş sayfasına yönlendirildi (authwall) - Atlanıyor")
                return None
            else:
                print("⚠️  LinkedIn giriş sayfasına yönlendirildi")
                print("💡 Manuel olarak giriş yapın, sonra Enter'a basın...")
                input("Enter'a basın...")

        # Sayfanın HTML'ini al
        html = driver.page_source
        return html

    except Exception as e:
        print(f"❌ LinkedIn sayfası yükleme hatası: {e}")
        return None
def extract_linkedin_info_detailed(html):
    """HTML'den detaylı LinkedIn firma bilgilerini çıkarır"""
    soup = BeautifulSoup(html, 'html.parser')

    info = {
        'name': '',
        'about': '',
        'tagline': '',
        'industry': '',
        'company_size': '',
        'headquarters': '',
        'founded': '',
        'website': '',
        'specialties': []
    }

    try:
        # Firma adı - h1 tag'inden veya meta'dan
        h1 = soup.find('h1', class_=re.compile(r'org.*-top-card.*name|company.*name'))
        if h1:
            info['name'] = h1.get_text(strip=True)

        if not info['name']:
            og_title = soup.find('meta', property='og:title')
            if og_title:
                title = og_title.get('content', '')
                info['name'] = title.split('|')[0].strip()

        # Tagline/Catchphrase
        tagline_elem = soup.find('p', class_=re.compile(r'org.*-top-card.*tagline|company.*tagline'))
        if tagline_elem:
            info['tagline'] = tagline_elem.get_text(strip=True)

        # About/Description
        about_section = soup.find('section', class_=re.compile(r'about.*section'))
        if about_section:
            about_text = about_section.find('p', class_=re.compile(r'break.*words|description'))
            if about_text:
                info['about'] = about_text.get_text(strip=True)

        # Alternatif about
        if not info['about']:
            og_desc = soup.find('meta', property='og:description')
            if og_desc:
                raw_about = og_desc.get('content', '').strip()
                # Temizle
                raw_about = re.sub(r"^.*?\s*\|\s*LinkedIn'de\s+[\d\.,]+\s+takipçi\s+", '', raw_about)
                info['about'] = raw_about.strip()

        # Company details (Industry, Size, etc.)
        detail_items = soup.find_all('dd', class_=re.compile(r'org.*-details|company.*-details'))
        for item in detail_items:
            text = item.get_text(strip=True)

            # Industry
            parent = item.find_parent('div')
            if parent:
                dt = parent.find('dt')
                if dt and 'Industry' in dt.get_text():
                    info['industry'] = text
                elif dt and 'Company size' in dt.get_text():
                    info['company_size'] = text
                elif dt and 'Headquarters' in dt.get_text():
                    info['headquarters'] = text
                elif dt and 'Founded' in dt.get_text():
                    info['founded'] = text

        # Website
        website_link = soup.find('a', class_=re.compile(r'org.*-website|company.*-website'))
        if website_link:
            info['website'] = website_link.get('href', '')

        # Specialties
        specialties_section = soup.find('section', class_=re.compile(r'specialties'))
        if specialties_section:
            specialty_items = specialties_section.find_all('li')
            info['specialties'] = [item.get_text(strip=True) for item in specialty_items]

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


def process_single_file(driver, json_path, args):
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
    html = fetch_linkedin_with_selenium(driver, linkedin_url, timeout=args.timeout, skip_on_auth=not args.manual_login)

    if not html:
        print("❌ LinkedIn HTML çekilemedi (authwall veya hata)")
        return False    # Bilgileri çıkar
    linkedin_info = extract_linkedin_info_detailed(html)

    print(f"\n✅ LinkedIn'den çekilen bilgiler:")
    print(f"  Name: {linkedin_info['name'] or '(bulunamadı)'}")
    print(f"  Tagline: {linkedin_info['tagline'] or '(bulunamadı)'}")
    print(f"  About: {linkedin_info['about'][:100] if linkedin_info['about'] else '(bulunamadı)'}{'...' if len(linkedin_info['about']) > 100 else ''}")
    if linkedin_info['industry']:
        print(f"  Industry: {linkedin_info['industry']}")
    if linkedin_info['company_size']:
        print(f"  Company Size: {linkedin_info['company_size']}")

    # JSON'u güncelle
    success = update_company_json_with_linkedin(json_path, linkedin_info, dry_run=args.dry_run, force=args.force)

    return success


def process_all_files(driver, args):
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
            success = process_single_file(driver, json_path, args)
            if success:
                stats['success'] += 1
            else:
                stats['skipped'] += 1
        except Exception as e:
            print(f"❌ Hata: {e}")
            stats['failed'] += 1

        # Rate limiting
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

    parser = argparse.ArgumentParser(description='LinkedIn firma bilgilerini Selenium ile çeker')
    parser.add_argument('json_file', nargs='?', help='İşlenecek JSON dosyası')
    parser.add_argument('--all', action='store_true', help='Tüm company JSON dosyalarını işle')
    parser.add_argument('--limit', type=int, help='İşlenecek maksimum dosya sayısı')
    parser.add_argument('--dry-run', action='store_true', help='Sadece göster, dosyayı güncelleme')
    parser.add_argument('--force', action='store_true', help='Mevcut bilgilerin üzerine yaz')
    parser.add_argument('--timeout', type=int, default=30, help='Sayfa yükleme timeout (saniye)')
    parser.add_argument('--delay', type=int, default=5, help='Dosyalar arası bekleme süresi (saniye)')
    parser.add_argument('--profile', type=str, help='Chrome/Opera profil dizini (ör: C:\\Users\\YourName\\AppData\\Local\\Google\\Chrome\\User Data)')
    parser.add_argument('--manual-login', action='store_true', help='Authwall durumunda manuel giriş bekle')
    parser.add_argument('--headless', action='store_true', help='Tarayıcıyı arka planda çalıştır (görünmez mod)')

    args = parser.parse_args()

    print("🌐 Tarayıcı başlatılıyor...")

    # WebDriver oluştur
    driver = create_driver(
        use_existing_profile=bool(args.profile),
        profile_path=args.profile,
        headless=args.headless
    )

    if not driver:
        return 1

    try:
        # Tüm dosyaları işle
        if args.all or not args.json_file:
            process_all_files(driver, args)
            return 0

        # Tek dosya işle
        json_path = Path(args.json_file)
        if not json_path.exists():
            alt_path = Path('public/data/company') / json_path.name
            if alt_path.exists():
                json_path = alt_path
            else:
                print(f"❌ Dosya bulunamadı: {args.json_file}")
                return 1

        success = process_single_file(driver, json_path, args)
        return 0 if success else 1

    finally:
        print("\n🔴 Tarayıcı kapatılıyor...")
        driver.quit()


if __name__ == '__main__':
    sys.exit(main())
