#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn linki eksik firmaları CSV formatında export eder
"""

import json
import csv
from pathlib import Path

def export_missing_linkedin():
    companies = []
    missing_file = Path('missing-linkedin.txt')

    # Dosya adlarını oku
    with open(missing_file, 'r', encoding='utf-8') as f:
        filenames = [line.strip() for line in f if line.strip()]

    print(f"📁 {len(filenames)} dosya okunuyor...\n")

    # Her firma için bilgileri topla
    for filename in filenames:
        json_path = Path('public/data/company') / f'{filename}.json'
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    companies.append({
                        'Sıra': len(companies) + 1,
                        'Firma Adı': data.get('name', ''),
                        'Dosya': filename,
                        'Web Sitesi': data.get('contact', {}).get('web', ''),
                        'Sektör': data.get('sector', ''),
                        'Şehir': data.get('location', {}).get('city', ''),
                        'X/Twitter': data.get('social', {}).get('x', '') if data.get('social') else '',
                        'Instagram': data.get('social', {}).get('instagram', '') if data.get('social') else '',
                        'Facebook': data.get('social', {}).get('facebook', '') if data.get('social') else ''
                    })
            except Exception as e:
                print(f"⚠️  Hata ({filename}): {e}")

    # CSV'ye kaydet
    csv_file = 'linkedin-eksik-firmalar.csv'
    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        if companies:
            fieldnames = ['Sıra', 'Firma Adı', 'Dosya', 'Web Sitesi', 'Sektör', 'Şehir', 'X/Twitter', 'Instagram', 'Facebook']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(companies)

    print(f"✅ {len(companies)} firma kaydedildi: {csv_file}\n")

    # Özet bilgi
    print("=" * 80)
    print("📊 LİNKEDIN LİNKİ EKSİK FİRMALAR")
    print("=" * 80)
    print(f"\nToplam: {len(companies)} firma\n")

    # İlk 15 firmayı göster
    print("İlk 15 Firma:")
    print("-" * 80)
    for i, comp in enumerate(companies[:15], 1):
        name = comp['Firma Adı'][:40].ljust(40)
        web = comp['Web Sitesi'][:35]
        print(f"{i:2}. {name} {web}")

    if len(companies) > 15:
        print(f"\n... ve {len(companies) - 15} firma daha")

    # Sektör bazlı istatistik
    sectors = {}
    for comp in companies:
        sector = comp['Sektör'] or 'Belirtilmemiş'
        sectors[sector] = sectors.get(sector, 0) + 1

    print(f"\n\n📈 Sektör Bazlı Dağılım (İlk 10):")
    print("-" * 80)
    for i, (sector, count) in enumerate(sorted(sectors.items(), key=lambda x: x[1], reverse=True)[:10], 1):
        sector_name = sector[:50].ljust(50)
        print(f"{i:2}. {sector_name} {count:3} firma")

    # Şehir bazlı istatistik
    cities = {}
    for comp in companies:
        city = comp['Şehir'] or 'Belirtilmemiş'
        cities[city] = cities.get(city, 0) + 1

    print(f"\n\n🏙️  Şehir Bazlı Dağılım (İlk 10):")
    print("-" * 80)
    for i, (city, count) in enumerate(sorted(cities.items(), key=lambda x: x[1], reverse=True)[:10], 1):
        city_name = city[:50].ljust(50)
        print(f"{i:2}. {city_name} {count:3} firma")

    # Sosyal medya durumu
    has_x = sum(1 for c in companies if c['X/Twitter'])
    has_insta = sum(1 for c in companies if c['Instagram'])
    has_fb = sum(1 for c in companies if c['Facebook'])

    print(f"\n\n📱 Diğer Sosyal Medya Hesapları:")
    print("-" * 80)
    print(f"   X/Twitter  : {has_x:3} firma ({has_x*100//len(companies)}%)")
    print(f"   Instagram  : {has_insta:3} firma ({has_insta*100//len(companies)}%)")
    print(f"   Facebook   : {has_fb:3} firma ({has_fb*100//len(companies)}%)")

    print(f"\n{'=' * 80}\n")
    print(f"💾 Detaylı liste: {csv_file}")
    print()

if __name__ == '__main__':
    export_missing_linkedin()
