#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download logos for companies that are missing them
"""

import sys
from pathlib import Path
import importlib.util

# Load the downloader module dynamically
spec = importlib.util.spec_from_file_location(
    "download_company_logos",
    Path(__file__).parent / "download-company-logos.py"
)
downloader_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(downloader_module)
LogoDownloader = downloader_module.LogoDownloader

def main():
    downloader = LogoDownloader()

    # Read missing logos list
    missing_logos_file = Path(__file__).parent.parent / 'missing-logos.txt'

    if not missing_logos_file.exists():
        print("ERROR: missing-logos.txt not found!")
        return

    with open(missing_logos_file, 'r', encoding='utf-8') as f:
        missing_slugs = [line.strip() for line in f if line.strip()]

    print(f"Processing {len(missing_slugs)} companies without logos...")
    print("="*60)

    success_count = 0
    failed_count = 0

    for i, slug in enumerate(missing_slugs, 1):
        json_file = downloader.company_dir / f"{slug}.json"

        if not json_file.exists():
            print(f"[{i}/{len(missing_slugs)}] SKIP: {slug} (JSON not found)")
            continue

        print(f"\n[{i}/{len(missing_slugs)}] Processing: {slug}")

        try:
            if downloader.process_company(json_file):
                success_count += 1
                print(f"  SUCCESS: Logo downloaded")
            else:
                failed_count += 1
                print(f"  FAILED: Could not download logo")
        except Exception as e:
            failed_count += 1
            print(f"  ERROR: {str(e)}")

    print("\n" + "="*60)
    print(f"RESULTS:")
    print(f"  Success: {success_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total: {success_count + failed_count}")
    print(f"  Success Rate: {success_count/(success_count+failed_count)*100:.1f}%")
    print("="*60)

if __name__ == '__main__':
    main()
