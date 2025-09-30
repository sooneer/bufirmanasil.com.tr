#!/usr/bin/env python3
"""Simple logo downloader - downloads missing logos in batch"""

import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import time
import warnings
warnings.filterwarnings('ignore')

class SimpleLogoDownloader:
    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.company_dir = self.root / 'public' / 'data' / 'company'
        self.logo_dir = self.root / 'public' / 'img' / 'company'
        self.logo_dir.mkdir(parents=True, exist_ok=True)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/121.0'
        }

    def find_logo(self, url):
        """Find and download logo from URL"""
        try:
            r = requests.get(url, headers=self.headers, timeout=10, verify=False)
            soup = BeautifulSoup(r.text, 'lxml')

            # Try to find SVG logo first
            for sel in ['img[src*=".svg"][class*="logo"]', 'img[class*="logo"]', 'img[id*="logo"]']:
                img = soup.select_one(sel)
                if img and img.get('src'):
                    src = img.get('src')
                    if not src.startswith('data:'):
                        return urljoin(url, src)

            # Try favicon
            fav = soup.find('link', rel='icon')
            if fav and fav.get('href'):
                return urljoin(url, fav['href'])

            return None
        except:
            return None

    def download_logo(self, url, slug):
        """Download logo file"""
        try:
            r = requests.get(url, headers=self.headers, timeout=10, verify=False, stream=True)
            if r.status_code != 200:
                return None

            # Determine extension
            ext = '.png'
            if '.svg' in url.lower():
                ext = '.svg'
            elif '.jpg' in url.lower() or '.jpeg' in url.lower():
                ext = '.jpg'
            elif '.webp' in url.lower():
                ext = '.webp'

            # Save file
            filepath = self.logo_dir / f"{slug}{ext}"
            filepath.write_bytes(r.content)

            return f"img/company/{slug}{ext}"
        except:
            return None

    def update_json(self, slug, logo_path):
        """Update JSON with logo path"""
        try:
            json_file = self.company_dir / f"{slug}.json"
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data['logo'] = logo_path

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True
        except:
            return False

    def process_company(self, slug):
        """Process one company"""
        # Check if logo exists
        for ext in ['.svg', '.png', '.jpg', '.jpeg', '.webp']:
            if (self.logo_dir / f"{slug}{ext}").exists():
                return 'exists'

        # Get company data
        json_file = self.company_dir / f"{slug}.json"
        if not json_file.exists():
            return 'no_json'

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        web = data.get('contact', {}).get('web', '')
        if not web:
            return 'no_web'

        # Find logo URL
        logo_url = self.find_logo(web)
        if not logo_url:
            return 'not_found'

        # Download logo
        logo_path = self.download_logo(logo_url, slug)
        if not logo_path:
            return 'download_failed'

        # Update JSON
        if not self.update_json(slug, logo_path):
            return 'json_update_failed'

        return 'success'

    def process_all(self, slugs):
        """Process list of company slugs"""
        results = {
            'success': 0,
            'exists': 0,
            'not_found': 0,
            'download_failed': 0,
            'no_web': 0,
            'no_json': 0,
            'json_update_failed': 0
        }

        for i, slug in enumerate(slugs, 1):
            result = self.process_company(slug)
            results[result] = results.get(result, 0) + 1

            if i % 10 == 0:
                print(f"[{i}/{len(slugs)}] Success: {results['success']}, Exists: {results['exists']}, Failed: {results['not_found'] + results['download_failed']}")

            if result == 'success':
                time.sleep(0.5)

        return results

# Main execution
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=None, help='Limit number of companies to process')
    args = parser.parse_args()

    downloader = SimpleLogoDownloader()

    # Read missing logos list
    missing_file = Path(__file__).parent.parent / 'missing-logos.txt'
    with open(missing_file, 'r', encoding='utf-8') as f:
        slugs = [line.strip() for line in f if line.strip()]

    if args.limit:
        slugs = slugs[:args.limit]

    print(f"Processing {len(slugs)} companies...")
    try:
        results = downloader.process_all(slugs)

        print("\nFinal Results:")
        print(f"  Success: {results['success']}")
        print(f"  Already exists: {results['exists']}")
        print(f"  Not found: {results['not_found']}")
        print(f"  Download failed: {results['download_failed']}")
        print(f"  No website: {results['no_web']}")
        print(f"  No JSON: {results['no_json']}")
        print(f"  JSON update failed: {results['json_update_failed']}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
