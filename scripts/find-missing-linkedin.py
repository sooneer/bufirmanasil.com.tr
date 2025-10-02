#!/usr/bin/env python3
"""
LinkedIn linki olmayan şirketleri listeler
"""

import json
from pathlib import Path

def find_companies_without_linkedin():
    """LinkedIn linki olmayan şirketleri bul"""
    company_dir = Path('public/data/company')

    if not company_dir.exists():
        print(f"❌ Dizin bulunamadı: {company_dir}")
        return

    json_files = sorted(company_dir.glob('*.json'))
    missing_linkedin = []

    print(f"🔍 {len(json_files)} şirket dosyası taranıyor...\n")

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            company_name = data.get('name', json_file.stem)
            linkedin = data.get('social', {}).get('linkedin', '').strip()

            if not linkedin:
                web = data.get('contact', {}).get('web', 'N/A')
                missing_linkedin.append({
                    'file': json_file.stem,
                    'name': company_name,
                    'web': web
                })
        except Exception as e:
            print(f"⚠️  Hata ({json_file.name}): {e}")

    # Sonuçları yazdır
    print("="*80)
    print(f"📊 LINKEDIN LİNKİ OLMAYAN ŞİRKETLER")
    print("="*80)
    print(f"\nToplam: {len(missing_linkedin)}/{len(json_files)} şirket\n")
    print("-"*80)

    for i, company in enumerate(missing_linkedin, 1):
        print(f"{i:3}. {company['name']}")
        print(f"     📄 Dosya: {company['file']}.json")
        print(f"     🌐 Web: {company['web']}")
        print()

    # Dosya isimlerini txt olarak kaydet
    output_file = 'missing-linkedin.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for company in missing_linkedin:
            f.write(f"{company['file']}\n")

    print("="*80)
    print(f"✅ Liste kaydedildi: {output_file}")
    print(f"💡 Toplu güncelleme için:")
    print(f"   python scripts/batch-update-simple.py --limit {len(missing_linkedin)}")
    print("="*80)

if __name__ == '__main__':
    find_companies_without_linkedin()
