#!/usr/bin/env python3
"""
company/klasöründeki JSON dosyalarından şirket listesi oluşturur
Her şirket için: name, slug (dosya adı), web sitesi bilgisi
"""

import json
import os
from pathlib import Path

def load_company_json(file_path):
    """JSON dosyasını yükle"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Hata ({file_path}): {e}")
        return None

def generate_companies_list(data_dir, output_file):
    """Şirket listesi oluştur"""
    company_files = sorted(Path(data_dir).glob('*.json'))
    companies = []

    print(f"🔍 {len(company_files)} şirket dosyası bulundu\n")

    for file_path in company_files:
        company_data = load_company_json(file_path)
        if not company_data:
            continue

        # Slug = dosya adı (uzantısız)
        slug = file_path.stem
        name = company_data.get('name', '')
        web = company_data.get('contact', {}).get('web', '')

        # Logo path
        logo = f"img/company/{slug}.svg"

        company_info = {
            'slug': slug,
            'name': name,
            'web': web,
            'logo': logo
        }

        companies.append(company_info)
        print(f"✅ {slug:30} => {name}")

    # JSON olarak kaydet
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*80}")
    print(f"✅ {len(companies)} şirket kaydedildi: {output_file}")
    print(f"{'='*80}\n")

    # Örnek kullanım
    print("📋 İlk 5 şirket:")
    for company in companies[:5]:
        print(f"   {company['slug']:30} | {company['name']}")

    print("\n💡 Kullanım örnekleri:")
    print("   - Angular component'te kullanım:")
    print("     companies: Company[] = [];")
    print("     // HTTP ile yükle: this.http.get<Company[]>('data/companies.json')")
    print("\n   - Filtreleme:")
    print("     const company = companies.find(c => c.slug === 'ado-bilisim');")
    print("\n   - Link oluşturma:")
    print("     <a [routerLink]=\"['/company', company.slug]\">{{ company.name }}</a>")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Şirket listesi oluştur')
    parser.add_argument('--data-dir', type=str, default='public/data/company',
                        help='Şirket JSON dosyalarının bulunduğu dizin')
    parser.add_argument('--output', type=str, default='public/data/companies.json',
                        help='Çıktı dosyası')

    args = parser.parse_args()

    generate_companies_list(args.data_dir, args.output)

if __name__ == '__main__':
    main()
