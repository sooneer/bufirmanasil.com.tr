#!/usr/bin/env python3
"""
Company Logo Downloader
Downloads company logos from their websites and updates JSON files
"""

import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse
import time
import mimetypes
from PIL import Image
import io
import sys
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

class LogoDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })
        # Disable SSL verification for problematic sites
        self.session.verify = False

        self.root_dir = Path(__file__).parent.parent
        self.company_dir = self.root_dir / 'public' / 'data' / 'company'
        self.logo_dir = self.root_dir / 'public' / 'img' / 'company'
        self.logo_dir.mkdir(parents=True, exist_ok=True)

    def find_logo_url(self, html_content, base_url):
        """Find logo URL from HTML content"""
        soup = BeautifulSoup(html_content, 'lxml')

        # Strategy 1: Look for SVG logos first (best quality)
        logo_selectors_svg = [
            'img[src*=".svg"][class*="logo"]',
            'img[src*=".svg"][id*="logo"]',
            'img[src*="logo"][src*=".svg"]',
            'a[class*="logo"] img[src*=".svg"]',
        ]

        for selector in logo_selectors_svg:
            img = soup.select_one(selector)
            if img and img.get('src'):
                return urljoin(base_url, img['src'])

        # Strategy 2: Look for logo in common class names
        logo_selectors = [
            'img[class*="logo"]',
            'img[id*="logo"]',
            'img[alt*="logo"]',
            'a[class*="logo"] img',
            '.logo img',
            '#logo img',
            '.site-logo img',
            '.brand img',
            '.navbar-brand img',
            'header img[class*="logo"]',
            'nav img[class*="logo"]'
        ]

        for selector in logo_selectors:
            img = soup.select_one(selector)
            if img and img.get('src'):
                src = img.get('src')
                # Skip data URIs and very small images
                if src.startswith('data:') or 'placeholder' in src.lower():
                    continue
                return urljoin(base_url, src)

        # Strategy 3: Look for og:image meta tag
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return urljoin(base_url, og_image['content'])

        # Strategy 4: Look for twitter:image meta tag
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image and twitter_image.get('content'):
            return urljoin(base_url, twitter_image['content'])

        # Strategy 5: Look for favicon (apple-touch-icon is usually higher quality)
        apple_icon = soup.find('link', rel='apple-touch-icon')
        if apple_icon and apple_icon.get('href'):
            return urljoin(base_url, apple_icon['href'])

        # Strategy 6: Look for regular favicon
        favicon = soup.find('link', rel='icon')
        if favicon and favicon.get('href'):
            return urljoin(base_url, favicon['href'])

        # Strategy 7: Try default favicon location
        return urljoin(base_url, '/favicon.ico')

    def get_extension_from_url(self, url, content_type=None):
        """Determine file extension from URL or content type"""
        if content_type:
            # Only use content type for known image types
            if 'image/' in content_type:
                ext = mimetypes.guess_extension(content_type.split(';')[0])
                if ext and ext in ['.svg', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.ico']:
                    return ext

        # Try to get from URL
        parsed = urlparse(url)
        path = parsed.path.lower()

        for ext in ['.svg', '.png', '.jpg', '.jpeg', '.webp', '.ico', '.gif']:
            if ext in path:
                return ext

        return '.png'  # Default to PNG    def download_and_save_logo(self, logo_url, company_slug, timeout=10):
        """Download logo and save with appropriate extension"""
        try:
            response = self.session.get(logo_url, timeout=timeout, stream=True, verify=False)
            response.raise_for_status()

            content_type = response.headers.get('content-type', '')

            # Get extension
            ext = self.get_extension_from_url(logo_url, content_type)

            # Special handling for SVG
            if 'svg' in content_type or ext == '.svg':
                logo_path = self.logo_dir / f"{company_slug}.svg"
                logo_path.write_bytes(response.content)
                return f"img/company/{company_slug}.svg"

            # For images, try to convert to optimal format
            try:
                img = Image.open(io.BytesIO(response.content))

                # Convert RGBA to RGB if saving as JPEG
                if img.mode == 'RGBA':
                    # Save as PNG to preserve transparency
                    logo_path = self.logo_dir / f"{company_slug}.png"
                    img.save(logo_path, 'PNG', optimize=True)
                    return f"img/company/{company_slug}.png"
                else:
                    # Save as JPEG for smaller file size
                    logo_path = self.logo_dir / f"{company_slug}.jpg"
                    img.convert('RGB').save(logo_path, 'JPEG', quality=85, optimize=True)
                    return f"img/company/{company_slug}.jpg"

            except Exception as e:
                # If image processing fails, save as-is
                logo_path = self.logo_dir / f"{company_slug}{ext}"
                logo_path.write_bytes(response.content)
                return f"img/company/{company_slug}{ext}"

        except Exception as e:
            return None

    def process_company(self, json_file):
        """Process a single company"""
        try:
            # Read company data
            with open(json_file, 'r', encoding='utf-8') as f:
                company_data = json.load(f)

            company_name = company_data.get('name', '')
            company_slug = json_file.stem
            web_url = company_data.get('contact', {}).get('web', '')

            if not web_url:
                return False

            # Check if logo already exists
            existing_logo = None
            for ext in ['.svg', '.png', '.jpg', '.jpeg', '.webp']:
                logo_path = self.logo_dir / f"{company_slug}{ext}"
                if logo_path.exists():
                    existing_logo = f"img/company/{company_slug}{ext}"

                    # Update JSON if needed
                    if company_data.get('logo') != existing_logo:
                        company_data['logo'] = existing_logo
                        with open(json_file, 'w', encoding='utf-8') as f:
                            json.dump(company_data, f, ensure_ascii=False, indent=2)
                    return True

            # Fetch website HTML
            try:
                # Suppress SSL warnings
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

                response = self.session.get(
                    web_url,
                    timeout=10,
                    allow_redirects=True,
                    verify=False,
                    headers={'Referer': 'https://www.google.com/'}
                )
                response.raise_for_status()
            except Exception as e:
                return False

            # Find logo URL
            logo_url = self.find_logo_url(response.text, response.url)
            if not logo_url:
                return False

            # Download and save logo
            logo_path = self.download_and_save_logo(logo_url, company_slug)
            if not logo_path:
                # Try alternative strategies if first attempt fails
                # Strategy: Try common logo paths
                base_domain = response.url.rstrip('/')
                alternative_urls = [
                    f"{base_domain}/logo.png",
                    f"{base_domain}/logo.svg",
                    f"{base_domain}/assets/logo.png",
                    f"{base_domain}/images/logo.png",
                    f"{base_domain}/img/logo.png",
                ]

                for alt_url in alternative_urls:
                    logo_path = self.download_and_save_logo(alt_url, company_slug)
                    if logo_path:
                        break

                if not logo_path:
                    return False

            # Update JSON file
            company_data['logo'] = logo_path
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(company_data, f, ensure_ascii=False, indent=2)

            # Be nice to servers
            time.sleep(1)

            return True

        except Exception as e:
            return False

    def process_all_companies(self, limit=None):
        """Process all companies"""
        json_files = sorted(list(self.company_dir.glob('*.json')))

        if limit:
            json_files = json_files[:limit]

        print(f"Toplam {len(json_files)} sirket islenecek\n")

        success_count = 0
        failed_count = 0

        for i, json_file in enumerate(json_files, 1):
            print(f"[{i}/{len(json_files)}] {json_file.stem}...", end=" ")


            if self.process_company(json_file):
                success_count += 1
                print("OK")
            else:
                failed_count += 1
                print("FAIL")

        print(f"\n{'='*60}")
        print(f"Basarili: {success_count}")
        print(f"Basarisiz: {failed_count}")
        print(f"Toplam: {success_count + failed_count}")
        print(f"{'='*60}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Download company logos from their websites')
    parser.add_argument('--limit', type=int, help='Limit number of companies to process')
    parser.add_argument('--company', type=str, help='Process specific company by slug')

    args = parser.parse_args()

    downloader = LogoDownloader()

    if args.company:
        json_file = downloader.company_dir / f"{args.company}.json"
        if json_file.exists():
            downloader.process_company(json_file)
        else:
            print(f"Sirket bulunamadi: {args.company}")
    else:
        downloader.process_all_companies(limit=args.limit)

if __name__ == '__main__':
    main()
