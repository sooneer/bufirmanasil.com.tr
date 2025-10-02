#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn linki olmayan firma dosyalarını siler
UYARI: Bu işlem geri alınamaz! Dikkatli kullanın.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

def delete_empty_linkedin_files(dry_run=True, create_backup=True):
    """LinkedIn alanı boş olan firma dosyalarını sil"""

    # Şirket dosyalarını bul
    company_dir = Path('public/data/company')
    if not company_dir.exists():
        print(f"❌ Dizin bulunamadı: {company_dir}")
        return

    # Yedek klasörü oluştur
    if create_backup and not dry_run:
        backup_dir = Path(f'backup_linkedin_empty_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        backup_dir.mkdir(exist_ok=True)
        print(f"📦 Yedek klasörü: {backup_dir}\n")

    json_files = sorted(company_dir.glob('*.json'))
    print(f"🔍 {len(json_files)} şirket dosyası taranıyor...\n")

    to_delete = []
    errors = []

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Social alanını kontrol et
            social = data.get('social')

            # Social alanı yoksa veya None ise
            if social is None:
                to_delete.append({
                    'file': json_file,
                    'name': data.get('name', ''),
                    'reason': 'social alanı yok'
                })
                continue

            # Social dict değilse
            if not isinstance(social, dict):
                to_delete.append({
                    'file': json_file,
                    'name': data.get('name', ''),
                    'reason': f'social alanı dict değil'
                })
                continue

            # LinkedIn alanını kontrol et
            linkedin = social.get('linkedin', '').strip() if isinstance(social.get('linkedin'), str) else ''

            if not linkedin:
                to_delete.append({
                    'file': json_file,
                    'name': data.get('name', ''),
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
    print("🗑️  SİLİNECEK DOSYALAR")
    print("=" * 80)
    print(f"\nToplam: {len(to_delete)}/{len(json_files)} dosya\n")

    if dry_run:
        print("⚠️  DRY RUN MODU - Hiçbir dosya silinmeyecek!\n")
    else:
        print("🔴 GERÇEK MOD - Dosyalar silinecek!\n")

    print("-" * 80)

    # İlk 30'u göster
    for i, item in enumerate(to_delete[:30], 1):
        name = item['name'][:35].ljust(35) if item['name'] else '(İsim yok)'.ljust(35)
        file = item['file'].stem[:25]
        print(f"{i:3}. {name} | {file}")

    if len(to_delete) > 30:
        print(f"\n... ve {len(to_delete) - 30} dosya daha")

    print("\n" + "=" * 80)

    # Silme işlemi
    if not dry_run:
        print("\n🗑️  Dosyalar siliniyor...\n")
        deleted_count = 0

        for item in to_delete:
            try:
                file_path = item['file']

                # Yedek al
                if create_backup:
                    backup_path = backup_dir / file_path.name
                    shutil.copy2(file_path, backup_path)

                # Sil
                file_path.unlink()
                deleted_count += 1
                print(f"  ✓ Silindi: {file_path.stem}")

            except Exception as e:
                print(f"  ✗ Hata ({file_path.stem}): {e}")

        print(f"\n✅ {deleted_count} dosya silindi")

        if create_backup:
            print(f"📦 Yedek: {backup_dir}")
    else:
        print("\n💡 Gerçekten silmek için:")
        print("   python scripts/delete-empty-linkedin-files.py --confirm")

    print()

    return to_delete

def main():
    import argparse

    parser = argparse.ArgumentParser(description='LinkedIn linki olmayan firma dosyalarını sil')
    parser.add_argument('--confirm', action='store_true', help='Gerçekten sil (DRY RUN değil)')
    parser.add_argument('--no-backup', action='store_true', help='Yedek alma')

    args = parser.parse_args()

    dry_run = not args.confirm
    create_backup = not args.no_backup

    if args.confirm:
        print("\n" + "=" * 80)
        print("⚠️  UYARI: Bu işlem geri alınamaz!")
        print("=" * 80)
        response = input("\nDevam etmek istiyor musunuz? (evet/hayır): ")

        if response.lower() not in ['evet', 'yes', 'e', 'y']:
            print("\n❌ İşlem iptal edildi.")
            return
        print()

    delete_empty_linkedin_files(dry_run=dry_run, create_backup=create_backup)

if __name__ == '__main__':
    main()
