#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
public/data/company klasöründeki JSON dosyalarında
LinkedIn alanı boş olan firmaları listeler
"""

import json
from pathlib import Path

def check_empty_linkedin():
    """LinkedIn alanı boş olan firmaları bul"""

    # Şirket dosyalarını bul
    company_dir = Path('public/data/company')
    if not company_dir.exists():
        print(f"❌ Dizin bulunamadı: {company_dir}")
        return []

    json_files = sorted(company_dir.glob('*.json'))
    print(f"🔍 {len(json_files)} şirket dosyası taranıyor...\n")

    empty_linkedin = []
    errors = []

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Social alanını kontrol et
            social = data.get('social')

            # Social alanı yoksa veya None ise
            if social is None:
                empty_linkedin.append({
                    'file': json_file.stem,
                    'name': data.get('name', ''),
                    'web': data.get('contact', {}).get('web', ''),
                    'reason': 'social alanı yok'
                })
                continue

            # Social dict değilse
            if not isinstance(social, dict):
                empty_linkedin.append({
                    'file': json_file.stem,
                    'name': data.get('name', ''),
                    'web': data.get('contact', {}).get('web', ''),
                    'reason': f'social alanı dict değil: {type(social)}'
                })
                continue

            # LinkedIn alanını kontrol et
            linkedin = social.get('linkedin', '').strip()

            if not linkedin:
                empty_linkedin.append({
                    'file': json_file.stem,
                    'name': data.get('name', ''),
                    'web': data.get('contact', {}).get('web', ''),
                    'reason': 'linkedin alanı boş'
                })

        except Exception as e:
            errors.append({'file': json_file.stem, 'error': str(e)})

    # Hataları göster
    if errors:
        print("⚠️  Hatalar:")
        for err in errors:
            print(f"   • {err['file']}: {err['error']}")
        print()

    # Sonuçları göster
    print("=" * 80)
    print("📊 LİNKEDİN ALANI BOŞ OLAN FİRMALAR")
    print("=" * 80)
    print(f"\nToplam: {len(empty_linkedin)}/{len(json_files)} şirket\n")
    print("-" * 80)

    # İlk 20'yi göster
    for i, company in enumerate(empty_linkedin[:20], 1):
        name = company['name'][:35].ljust(35) if company['name'] else '(İsim yok)'.ljust(35)
        file = company['file'][:25].ljust(25)
        print(f"{i:3}. {name} | {file} | {company['reason']}")

    if len(empty_linkedin) > 20:
        print(f"\n... ve {len(empty_linkedin) - 20} firma daha")

    print("\n" + "=" * 80)

    # Sadece dosya isimlerini txt'ye kaydet
    output_file = 'empty-linkedin-files.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for company in empty_linkedin:
            f.write(f"{company['file']}\n")

    print(f"✅ Dosya isimleri kaydedildi: {output_file}")

    # Sebep bazlı istatistik
    reasons = {}
    for comp in empty_linkedin:
        reason = comp['reason']
        reasons[reason] = reasons.get(reason, 0) + 1

    print(f"\n📈 Sebep Bazlı Dağılım:")
    for reason, count in sorted(reasons.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {reason}: {count} firma")

    print()

    return empty_linkedin

if __name__ == '__main__':
    check_empty_linkedin()
