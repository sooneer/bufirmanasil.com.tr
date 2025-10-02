#!/usr/bin/env python3
"""
LinkedIn Link Lister
Tüm şirket JSON dosyalarındaki LinkedIn linklerini listeler.
"""

import json
from pathlib import Path

def main():
    company_dir = Path("public/data/company")

    # Tüm JSON dosyalarını oku
    json_files = sorted(company_dir.glob("*.json"))

    print(f"Toplam {len(json_files)} şirket dosyası bulundu.\n")
    print("=" * 80)

    has_linkedin = []
    no_linkedin = []

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            company_name = data.get('name', json_file.stem)
            linkedin = data.get('social', {}).get('linkedin', '')

            if linkedin:
                has_linkedin.append((json_file.stem, company_name, linkedin))
            else:
                no_linkedin.append((json_file.stem, company_name))

        except Exception as e:
            print(f"❌ Hata ({json_file.name}): {e}")

    # LinkedIn'i olanları yazdır
    print(f"\n✅ LinkedIn Linki Olan Şirketler ({len(has_linkedin)}):")
    print("=" * 80)
    for file_name, company_name, linkedin in has_linkedin:
        print(linkedin)

    # LinkedIn'i olmayanları yazdır
    print(f"\n\n❌ LinkedIn Linki Olmayan Şirketler ({len(no_linkedin)}):")
    print("=" * 80)
    for file_name, company_name in no_linkedin:
        print(f"{file_name:30} | {company_name}")

    # Özet
    print("\n" + "=" * 80)
    print(f"📊 ÖZET:")
    print(f"   Toplam Şirket: {len(json_files)}")
    print(f"   LinkedIn Var:  {len(has_linkedin)}")
    print(f"   LinkedIn Yok:  {len(no_linkedin)}")
    print("=" * 80)

    # Dosyaya kaydet
    output_file = "linkedin-links-list.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for file_name, company_name, linkedin in has_linkedin:
            f.write(f"{linkedin}\n")

    print(f"\n📄 Sonuçlar '{output_file}' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
