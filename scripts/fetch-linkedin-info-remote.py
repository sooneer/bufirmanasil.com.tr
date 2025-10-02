#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Firma Bilgisi Çekme Script (Remote Debugging)
Opera'da açık olan tarayıcı oturumunu kullanır.
"""

import json
import re
import sys
import time
import argparse
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


def connect_to_remote_browser(debugger_address='localhost:9222'):
    """Açık olan Opera tarayıcısına bağlan"""
    print(f"🔗 Remote tarayıcıya bağlanılıyor: {debugger_address}")

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)

    # WebDriver'ı başlat
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        print("✅ Tarayıcıya bağlandı!")
        return driver
    except Exception as e:
        print(f"❌ Tarayıcıya bağlanırken hata: {e}")
        print("\n💡 Opera'yı şu komutla başlatın:")
        print('   "C:\\Users\\soner.acar\\AppData\\Local\\Programs\\Opera\\opera.exe" --remote-debugging-port=9222 --user-data-dir="C:\\Users\\soner.acar\\AppData\\Roaming\\Opera Software\\Opera Stable"')
        return None


def extract_linkedin_info_from_page(driver, linkedin_url, timeout=30):
    """LinkedIn sayfasından bilgileri çıkar"""
    try:
        print(f"🔍 LinkedIn sayfası açılıyor: {linkedin_url}")
        driver.get(linkedin_url)

        # Sayfanın yüklenmesini bekle
        time.sleep(3)

        # Auth wall kontrolü
        if 'authwall' in driver.current_url.lower() or 'login' in driver.current_url.lower():
            print("⚠️  LinkedIn giriş ekranına yönlendirildi!")
            print("💡 Lütfen Opera'da LinkedIn'e giriş yapın ve scripti tekrar çalıştırın.")
            return None

        # Sayfa HTML'ini al
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        info = {
            'name': '',
            'about': '',
            'tagline': '',
            'industry': '',
            'company_size': '',
            'headquarters': '',
            'website': '',
            'founded': ''
        }

        # Firma adı
        try:
            # h1 başlıktan firma adını al
            name_elem = driver.find_element(By.CSS_SELECTOR, 'h1.org-top-card-summary__title')
            info['name'] = name_elem.text.strip()
            print(f"  ✓ Name: {info['name']}")
        except NoSuchElementException:
            # Alternatif selector'lar
            try:
                name_elem = driver.find_element(By.CSS_SELECTOR, 'h1')
                info['name'] = name_elem.text.strip()
            except:
                pass

        # Tagline
        try:
            tagline_elem = driver.find_element(By.CSS_SELECTOR, 'p.org-top-card-summary__tagline')
            info['tagline'] = tagline_elem.text.strip()
            print(f"  ✓ Tagline: {info['tagline']}")
        except NoSuchElementException:
            pass

        # About
        try:
            about_elem = driver.find_element(By.CSS_SELECTOR, 'p.break-words')
            info['about'] = about_elem.text.strip()
            print(f"  ✓ About: {info['about'][:100]}...")
        except NoSuchElementException:
            # Alternatif: section içinden about'u bul
            try:
                about_section = driver.find_element(By.CSS_SELECTOR, 'section[data-test-id="about-us"]')
                paragraphs = about_section.find_elements(By.TAG_NAME, 'p')
                if paragraphs:
                    info['about'] = '\n'.join([p.text.strip() for p in paragraphs if p.text.strip()])
                    print(f"  ✓ About: {info['about'][:100]}...")
            except:
                pass

        # Industry (Sektör)
        try:
            # "Sektör" veya "Industry" yazısını içeren dt elementi bul
            labels = driver.find_elements(By.CSS_SELECTOR, 'dt.org-page-details__definition-term')
            for label in labels:
                if 'Industry' in label.text or 'Sektör' in label.text:
                    # Hemen sonraki dd elementini al
                    industry_elem = label.find_element(By.XPATH, './following-sibling::dd')
                    info['industry'] = industry_elem.text.strip()
                    print(f"  ✓ Industry: {info['industry']}")
                    break
        except:
            pass

        # Company size (Çalışan sayısı)
        try:
            labels = driver.find_elements(By.CSS_SELECTOR, 'dt.org-page-details__definition-term')
            for label in labels:
                if 'Company size' in label.text or 'Şirket büyüklüğü' in label.text:
                    size_elem = label.find_element(By.XPATH, './following-sibling::dd')
                    info['company_size'] = size_elem.text.strip()
                    print(f"  ✓ Company Size: {info['company_size']}")
                    break
        except:
            pass

        # Headquarters (Genel merkez)
        try:
            labels = driver.find_elements(By.CSS_SELECTOR, 'dt.org-page-details__definition-term')
            for label in labels:
                if 'Headquarters' in label.text or 'Genel merkez' in label.text:
                    hq_elem = label.find_element(By.XPATH, './following-sibling::dd')
                    info['headquarters'] = hq_elem.text.strip()
                    print(f"  ✓ Headquarters: {info['headquarters']}")
                    break
        except:
            pass

        # Website
        try:
            labels = driver.find_elements(By.CSS_SELECTOR, 'dt.org-page-details__definition-term')
            for label in labels:
                if 'Website' in label.text or 'Web sitesi' in label.text:
                    web_elem = label.find_element(By.XPATH, './following-sibling::dd')
                    info['website'] = web_elem.text.strip()
                    print(f"  ✓ Website: {info['website']}")
                    break
        except:
            pass

        # Founded (Kuruluş yılı)
        try:
            labels = driver.find_elements(By.CSS_SELECTOR, 'dt.org-page-details__definition-term')
            for label in labels:
                if 'Founded' in label.text or 'Kuruluş' in label.text:
                    founded_elem = label.find_element(By.XPATH, './following-sibling::dd')
                    info['founded'] = founded_elem.text.strip()
                    print(f"  ✓ Founded: {info['founded']}")
                    break
        except:
            pass

        return info

    except Exception as e:
        print(f"❌ LinkedIn bilgi çekme hatası: {e}")
        import traceback
        traceback.print_exc()
        return None


def update_company_json_with_linkedin(json_path, linkedin_info, dry_run=False, force=False):
    """JSON dosyasını LinkedIn bilgileriyle günceller"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        updated = False
        updates = []

        # Name
        if linkedin_info.get('name') and (not data.get('name') or force):
            data['name'] = linkedin_info['name']
            updated = True
            updates.append(f"Name: {linkedin_info['name']}")

        # About
        if linkedin_info.get('about') and (not data.get('about') or force):
            data['about'] = linkedin_info['about']
            updated = True
            updates.append(f"About: {linkedin_info['about'][:100]}...")

        # Tagline
        if linkedin_info.get('tagline') and (not data.get('tagline') or force):
            data['tagline'] = linkedin_info['tagline']
            updated = True
            updates.append(f"Tagline: {linkedin_info['tagline']}")

        if not updated:
            print("  ℹ️  Güncellenecek yeni bilgi bulunamadı")
            return False

        print("\n📝 Güncellenecek alanlar:")
        for update in updates:
            print(f"  • {update}")

        if not dry_run:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n✅ Dosya güncellendi: {json_path}")
        else:
            print(f"\n🔍 DRY RUN: Dosya güncellenmedi")

        return True

    except Exception as e:
        print(f"❌ JSON güncelleme hatası: {e}")
        return False


def process_single_file(driver, json_path, args):
    """Tek bir JSON dosyasını işler"""
    print(f"\n{'='*70}")
    print(f"📂 Dosya: {json_path.name}")
    print(f"{'='*70}")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ JSON okuma hatası: {e}")
        return False

    linkedin_url = data.get('social', {}).get('linkedin', '')
    if not linkedin_url:
        print("⚠️  LinkedIn linki bulunamadı")
        return False

    print(f"🔗 LinkedIn: {linkedin_url}")

    # Mevcut bilgileri göster
    print(f"\n📊 Mevcut Bilgiler:")
    print(f"  Name: {data.get('name', '(boş)')}")
    print(f"  Tagline: {data.get('tagline', '(boş)')}")
    print(f"  About: {data.get('about', '(boş)')[:100]}...")

    # LinkedIn'den bilgi çek
    linkedin_info = extract_linkedin_info_from_page(driver, linkedin_url, timeout=args.timeout)

    if not linkedin_info:
        print("❌ LinkedIn bilgileri çekilemedi")
        return False

    # JSON'u güncelle
    success = update_company_json_with_linkedin(json_path, linkedin_info, dry_run=args.dry_run, force=args.force)

    return success


def process_all_files(driver, args):
    """Tüm company JSON dosyalarını işler"""
    company_dir = Path('public/data/company')

    if not company_dir.exists():
        print(f"❌ Klasör bulunamadı: {company_dir}")
        return

    json_files = sorted(company_dir.glob('*.json'))

    if not json_files:
        print(f"❌ JSON dosyası bulunamadı")
        return

    print(f"📁 Toplam {len(json_files)} dosya bulundu")

    if args.limit:
        json_files = json_files[:args.limit]
        print(f"⚠️  Limit: İlk {args.limit} dosya işlenecek")

    stats = {
        'total': len(json_files),
        'success': 0,
        'failed': 0,
        'skipped': 0
    }

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

        if i < len(json_files):
            wait_time = args.delay
            print(f"\n⏳ {wait_time} saniye bekleniyor...")
            time.sleep(wait_time)

    print(f"\n{'='*70}")
    print(f"📊 İŞLEM ÖZETİ")
    print(f"{'='*70}")
    print(f"Toplam: {stats['total']}")
    print(f"Başarılı: {stats['success']}")
    print(f"Atlandı: {stats['skipped']}")
    print(f"Hatalı: {stats['failed']}")
    print(f"{'='*70}")


def main():
    parser = argparse.ArgumentParser(description='LinkedIn firma bilgilerini çeker (Remote Debugging)')
    parser.add_argument('json_file', nargs='?', help='İşlenecek JSON dosyası')
    parser.add_argument('--all', action='store_true', help='Tüm company JSON dosyalarını işle')
    parser.add_argument('--limit', type=int, help='İşlenecek maksimum dosya sayısı')
    parser.add_argument('--dry-run', action='store_true', help='Sadece göster, dosyayı güncelleme')
    parser.add_argument('--force', action='store_true', help='Mevcut bilgilerin üzerine yaz')
    parser.add_argument('--timeout', type=int, default=30, help='Sayfa yükleme timeout')
    parser.add_argument('--delay', type=int, default=7, help='Dosyalar arası bekleme (saniye)')
    parser.add_argument('--debug-port', default='localhost:9222', help='Remote debugging address')

    args = parser.parse_args()

    # Remote tarayıcıya bağlan
    driver = connect_to_remote_browser(args.debug_port)
    if not driver:
        return 1

    try:
        if args.all or not args.json_file:
            process_all_files(driver, args)
        else:
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
        # Driver'ı kapatma - açık tarayıcıya bağlandığımız için kapatmıyoruz
        print("\n✅ İşlem tamamlandı!")

    return 0


if __name__ == '__main__':
    sys.exit(main())
