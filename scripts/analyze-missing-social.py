#!/usr/bin/env python3
"""
Şirket JSON dosyalarındaki eksik sosyal medya linklerini analiz eder
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def load_company_json(file_path):
    """JSON dosyasını yükle"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Hata ({file_path}): {e}")
        return None

def check_missing_social_links(company_data):
    """Eksik sosyal medya linklerini kontrol et"""
    social_platforms = ['linkedin', 'x', 'instagram', 'facebook', 'youtube', 'github']
    missing = []

    # Social alanını kontrol et
    social = company_data.get('social', {})
    if not social:
        social = {}

    for platform in social_platforms:
        link = social.get(platform)
        if not link or not str(link).strip():
            missing.append(platform)

    return missing

def analyze_all_companies(data_dir):
    """Tüm şirketleri analiz et"""
    company_files = list(Path(data_dir).glob('*.json'))

    stats = {
        'total': len(company_files),
        'with_missing': 0,
        'platform_stats': defaultdict(int),
        'companies_by_missing': defaultdict(list)
    }

    missing_details = []

    for file_path in sorted(company_files):
        company_data = load_company_json(file_path)
        if not company_data:
            continue

        missing = check_missing_social_links(company_data)

        if missing:
            stats['with_missing'] += 1
            company_name = company_data.get('name', file_path.stem)
            web = company_data.get('contact', {}).get('web', 'N/A')

            missing_details.append({
                'file': file_path.stem,
                'name': company_name,
                'web': web,
                'missing': missing,
                'missing_count': len(missing)
            })

            for platform in missing:
                stats['platform_stats'][platform] += 1

            # Eksik sayısına göre grupla
            stats['companies_by_missing'][len(missing)].append(file_path.stem)

    return stats, missing_details

def print_analysis(stats, missing_details):
    """Analiz sonuçlarını yazdır"""
    print("\n" + "="*80)
    print("📊 SOSYAL MEDYA LİNKLERİ ANALİZ RAPORU")
    print("="*80)

    print(f"\n📁 Toplam Şirket: {stats['total']}")
    print(f"⚠️  Eksik Linki Olan Şirket: {stats['with_missing']}")
    print(f"✅ Tamamı Dolu Olan Şirket: {stats['total'] - stats['with_missing']}")

    print("\n" + "-"*80)
    print("📊 PLATFORM BAZINDA EKSİK İSTATİSTİKLERİ")
    print("-"*80)

    sorted_platforms = sorted(stats['platform_stats'].items(), key=lambda x: x[1], reverse=True)
    for platform, count in sorted_platforms:
        percentage = (count / stats['total']) * 100
        print(f"  {platform:12} : {count:4} şirkette eksik ({percentage:5.1f}%)")

    print("\n" + "-"*80)
    print("📊 EKSİK LİNK SAYISINA GÖRE DAĞILIM")
    print("-"*80)

    for missing_count in sorted(stats['companies_by_missing'].keys(), reverse=True):
        companies = stats['companies_by_missing'][missing_count]
        print(f"  {missing_count} eksik link: {len(companies)} şirket")

    # En çok eksik olan 20 şirketi göster
    print("\n" + "-"*80)
    print("⚠️  EN ÇOK EKSİK LİNKİ OLAN İLK 20 ŞİRKET")
    print("-"*80)

    sorted_details = sorted(missing_details, key=lambda x: x['missing_count'], reverse=True)[:20]

    for i, detail in enumerate(sorted_details, 1):
        print(f"\n{i}. {detail['name']}")
        print(f"   📄 Dosya: {detail['file']}.json")
        print(f"   🌐 Web: {detail['web']}")
        print(f"   ⚠️  Eksik ({detail['missing_count']}): {', '.join(detail['missing'])}")

    # Batch komut önerileri
    print("\n" + "="*80)
    print("💡 TOPLU GÜNCELLEME ÖNERİLERİ")
    print("="*80)

    print("\n1️⃣  Tüm eksik linkleri güncelle:")
    print("   python scripts/batch-update-simple.py --limit 2000")

    print("\n2️⃣  Sadece web sitesi olan şirketleri güncelle:")
    print("   python scripts/batch-update-simple.py --limit 2000")

    print("\n3️⃣  Belirli şirketleri güncelle (örnekler):")
    if len(sorted_details) >= 5:
        example_companies = '|'.join([d['file'] for d in sorted_details[:5]])
        print(f'   python scripts/batch-update-simple.py --filter "{example_companies}"')

    # CSV olarak export
    print("\n" + "-"*80)
    print("💾 DETAYLI LİSTEYİ KAYDET")
    print("-"*80)
    print("   CSV formatında kaydetmek için:")
    print("   python scripts/analyze-missing-social.py --export missing-social-links.csv")

    return sorted_details

def export_to_csv(missing_details, output_file):
    """Eksik linkleri CSV olarak kaydet"""
    import csv

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Dosya', 'Şirket Adı', 'Web Sitesi', 'Eksik Link Sayısı', 'Eksik Linkler'])

        # Tüm şirketleri kaydet (sorted_details yerine missing_details kullan)
        for detail in sorted(missing_details, key=lambda x: x['missing_count'], reverse=True):
            writer.writerow([
                detail['file'] + '.json',
                detail['name'],
                detail['web'],
                detail['missing_count'],
                ', '.join(detail['missing'])
            ])

    print(f"\n✅ CSV dosyası kaydedildi: {output_file}")
    print(f"   Toplam {len(missing_details)} şirket listelendi\n")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Eksik sosyal medya linklerini analiz et')
    parser.add_argument('--export', type=str, help='CSV dosyası olarak export et')
    parser.add_argument('--data-dir', type=str, default='public/data/company',
                        help='Şirket JSON dosyalarının bulunduğu dizin')

    args = parser.parse_args()

    print("🔍 Şirket dosyaları taranıyor...\n")

    stats, missing_details = analyze_all_companies(args.data_dir)
    sorted_details = print_analysis(stats, missing_details)

    if args.export:
        # Export için orijinal missing_details kullan (tümü)
        export_to_csv(missing_details, args.export)

if __name__ == '__main__':
    main()
