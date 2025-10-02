#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
companies.json dosyasından silinen firmaları temizle
"""

import json
from pathlib import Path

def clean_companies_json():
    """companies.json'dan silinmiş firmaları temizle"""

    # Mevcut company dosyalarını al
    company_dir = Path('public/data/company')
    existing_files = {f.stem for f in company_dir.glob('*.json')}

    print(f"📁 Mevcut firma dosyası sayısı: {len(existing_files)}\n")

    # companies.json'u oku
    companies_json_path = Path('docs/data/companies.json')

    if not companies_json_path.exists():
        print(f"❌ {companies_json_path} bulunamadı!")
        return

    with open(companies_json_path, 'r', encoding='utf-8') as f:
        companies_data = json.load(f)

    original_count = len(companies_data)
    print(f"📊 companies.json'daki firma sayısı: {original_count}\n")

    # Silinecek firmaları bul
    to_remove = []
    cleaned_data = []

    for company in companies_data:
        # slug veya id alanını kullan
        company_slug = company.get('slug', company.get('id', ''))
        if company_slug in existing_files:
            cleaned_data.append(company)
        else:
            to_remove.append({
                'slug': company_slug,
                'name': company.get('name', ''),
                'sector': company.get('sector', '')
            })

    removed_count = len(to_remove)

    print("=" * 80)
    print(f"🗑️  companies.json'DAN SİLİNECEK FİRMALAR")
    print("=" * 80)
    print(f"\nToplam: {removed_count} firma\n")
    print("-" * 80)

    # İlk 30'u göster
    for i, company in enumerate(to_remove[:30], 1):
        name = company['name'][:40].ljust(40) if company['name'] else '(İsim yok)'.ljust(40)
        company_slug = company['slug'][:25]
        print(f"{i:3}. {name} | {company_slug}")

    if removed_count > 30:
        print(f"\n... ve {removed_count - 30} firma daha")

    print("\n" + "=" * 80)

    # Yedek al
    backup_path = companies_json_path.parent / 'companies.json.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(companies_data, f, ensure_ascii=False, indent=2)

    print(f"📦 Yedek alındı: {backup_path}")

    # Temizlenmiş veriyi kaydet
    with open(companies_json_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ companies.json güncellendi!")
    print(f"   Önceki: {original_count} firma")
    print(f"   Yeni:   {len(cleaned_data)} firma")
    print(f"   Silinen: {removed_count} firma")
    print()

if __name__ == '__main__':
    clean_companies_json()
