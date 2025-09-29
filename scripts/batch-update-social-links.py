#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toplu Sosyal Medya Linki Güncelleme Script'i
Tüm şirketler için sosyal medya linklerini günceller
"""

import json
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

def process_company(json_file, dry_run=False, timeout=10):
    """Bir şirket için sosyal medya linklerini güncelle"""
    company_name = json_file.stem

    # Python script'ini çalıştır
    python_exe = Path(sys.executable)
    script_path = Path(__file__).parent / 'update-social-links.py'

    cmd = [
        str(python_exe),
        str(script_path),
        str(json_file)
    ]

    if dry_run:
        cmd.append('--dry-run')

    cmd.extend(['--timeout', str(timeout)])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=timeout + 5,
            cwd=Path(__file__).parent.parent  # Workspace root
        )

        # Başarılı mı kontrol et
        success = result.returncode == 0

        # Output'u parse et
        output_lines = result.stdout.strip().split('\n')
        found_count = 0
        updated_count = 0

        for line in output_lines:
            if 'Toplam' in line and 'bulundu' in line:
                try:
                    found_count = int(line.split('Toplam')[1].split('sosyal')[0].strip())
                except:
                    pass
            if '📝' in line and 'güncellendi' in line:
                updated_count += 1

        return {
            'company': company_name,
            'success': success,
            'found': found_count,
            'updated': updated_count,
            'error': None if success else result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            'company': company_name,
            'success': False,
            'found': 0,
            'updated': 0,
            'error': 'Timeout'
        }
    except Exception as e:
        return {
            'company': company_name,
            'success': False,
            'found': 0,
            'updated': 0,
            'error': str(e)
        }

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Tüm şirketler için sosyal medya linklerini güncelle')
    parser.add_argument('--dry-run', action='store_true', help='Sadece göster, dosyaları güncelleme')
    parser.add_argument('--workers', type=int, default=5, help='Paralel işlem sayısı')
    parser.add_argument('--timeout', type=int, default=10, help='Her şirket için timeout (saniye)')
    parser.add_argument('--filter', help='Sadece belirli şirketleri işle (regex pattern)')

    args = parser.parse_args()

    # Şirket dosyalarını bul
    company_dir = Path('public/data/company')
    if not company_dir.exists():
        print(f"❌ Dizin bulunamadı: {company_dir}")
        return 1

    json_files = list(company_dir.glob('*.json'))

    # Filtrele
    if args.filter:
        import re
        pattern = re.compile(args.filter, re.IGNORECASE)
        json_files = [f for f in json_files if pattern.search(f.stem)]

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
        'errors': []
    }

    # İşle
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(process_company, json_file, args.dry_run, args.timeout): json_file
            for json_file in json_files
        }

        # Process results as they complete
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()

            print(f"[{i}/{len(json_files)}] {result['company']}", end=' ')

            if result['success']:
                stats['success'] += 1
                if result['found'] > 0:
                    stats['found_total'] += result['found']
                    stats['updated_total'] += result['updated']
                    print(f"✅ {result['found']} bulundu, {result['updated']} güncellendi")
                else:
                    print("⚪ Link bulunamadı")
            else:
                stats['failed'] += 1
                error_msg = result['error'][:50] if result['error'] else 'Unknown error'
                print(f"❌ Hata: {error_msg}")
                stats['errors'].append({
                    'company': result['company'],
                    'error': result['error']
                })

    # Özet
    print(f"\n" + "="*60)
    print(f"📊 ÖZET")
    print(f"="*60)
    print(f"Toplam Şirket     : {stats['total']}")
    print(f"Başarılı          : {stats['success']} ✅")
    print(f"Başarısız         : {stats['failed']} ❌")
    print(f"Toplam Link Bulundu : {stats['found_total']}")
    print(f"Toplam Güncelleme   : {stats['updated_total']}")

    if stats['errors']:
        print(f"\n⚠️  {len(stats['errors'])} şirkette hata oluştu:")
        for err in stats['errors'][:10]:  # İlk 10 hatayı göster
            print(f"  • {err['company']}: {err['error'][:80]}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
