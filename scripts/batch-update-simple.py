#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toplu Sosyal Medya Linki Güncelleme Script'i (Basit Versiyon)
"""

import sys
from pathlib import Path
import time

# update-social-links modülünü import et
import importlib.util
spec = importlib.util.spec_from_file_location("update_social_links", "scripts/update-social-links.py")
update_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update_module)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Tüm şirketler için sosyal medya linklerini güncelle')
    parser.add_argument('--dry-run', action='store_true', help='Sadece göster, dosyaları güncelleme')
    parser.add_argument('--timeout', type=int, default=10, help='Her şirket için timeout (saniye)')
    parser.add_argument('--filter', help='Sadece belirli şirketleri işle (kısmi isim)')
    parser.add_argument('--limit', type=int, help='İşlenecek maksimum şirket sayısı')

    args = parser.parse_args()

    # Şirket dosyalarını bul
    company_dir = Path('public/data/company')
    if not company_dir.exists():
        print(f"❌ Dizin bulunamadı: {company_dir}")
        return 1

    json_files = sorted(company_dir.glob('*.json'))

    # Filtrele
    if args.filter:
        json_files = [f for f in json_files if args.filter.lower() in f.stem.lower()]

    # Limit
    if args.limit:
        json_files = json_files[:args.limit]

    print(f"📁 Toplam {len(json_files)} şirket bulundu")

    if args.dry_run:
        print("🔍 DRY RUN modu aktif - dosyalar güncellenmeyecek\n")
    else:
        print("✍️  Dosyalar güncellenecek\n")

    # İstatistikler
    stats = {
        'total': len(json_files),
        'success': 0,
        'failed': 0,
        'found_total': 0,
        'updated_total': 0,
        'no_links': 0,
        'errors': []
    }

    # İşle
    for i, json_file in enumerate(json_files, 1):
        company_name = json_file.stem
        print(f"\n[{i}/{len(json_files)}] {company_name}")
        print("─" * 60)

        try:
            # JSON oku
            import json
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Web adresini al
            web_url = data.get('contact', {}).get('web', '')
            if not web_url:
                print(f"⚪ Web adresi yok")
                stats['no_links'] += 1
                continue

            print(f"🌐 {web_url}")

            # HTML'i çek
            html = update_module.fetch_html(web_url, timeout=args.timeout, verify_ssl=False)
            if not html:
                stats['failed'] += 1
                stats['errors'].append({'company': company_name, 'error': 'HTML çekilemedi'})
                continue

            # Sosyal medya linklerini çıkar
            social_links = update_module.extract_social_links(html, web_url)

            # Bulunan linkleri say
            found_count = sum(1 for link in social_links.values() if link)

            if found_count == 0:
                print(f"⚪ Sosyal medya linki bulunamadı")
                stats['no_links'] += 1
                stats['success'] += 1
                continue

            print(f"✅ {found_count} link bulundu")

            # JSON'u güncelle
            updated = update_module.update_company_json(json_file, social_links, dry_run=args.dry_run)

            if updated:
                stats['success'] += 1
                stats['found_total'] += found_count
                # Güncellenen sayıyı hesapla
                old_social = data.get('social', {})
                updated_count = sum(1 for platform, link in social_links.items()
                                   if link and not old_social.get(platform))
                stats['updated_total'] += updated_count
            else:
                stats['no_links'] += 1
                stats['success'] += 1

            # Rate limiting
            time.sleep(0.5)

        except Exception as e:
            stats['failed'] += 1
            print(f"❌ Hata: {str(e)[:100]}")
            stats['errors'].append({'company': company_name, 'error': str(e)[:100]})

    # Özet
    print(f"\n" + "="*60)
    print(f"📊 ÖZET")
    print(f"="*60)
    print(f"Toplam Şirket       : {stats['total']}")
    print(f"Başarılı            : {stats['success']} ✅")
    print(f"Başarısız           : {stats['failed']} ❌")
    print(f"Link Bulunamadı     : {stats['no_links']} ⚪")
    print(f"Toplam Link Bulundu : {stats['found_total']}")
    print(f"Toplam Güncelleme   : {stats['updated_total']}")

    if stats['errors']:
        print(f"\n⚠️  {len(stats['errors'])} şirkette hata:")
        for err in stats['errors'][:10]:
            print(f"  • {err['company']}: {err['error']}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
