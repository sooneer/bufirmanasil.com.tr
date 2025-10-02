#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sosyal Medya Linklerini Web Sitesinden Çeken Script
Web sitesinden sosyal medya linklerini bulup JSON dosyasını günceller.
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

# Sosyal medya platformları ve pattern'leri
SOCIAL_PATTERNS = {
    'linkedin': [
        r'linkedin\.com/company/([^/\s"\']+)',
        r'linkedin\.com/in/([^/\s"\']+)',
        r'tr\.linkedin\.com/company/([^/\s"\']+)'
    ],
    'x': [
        r'twitter\.com/([^/\s"\']+)',
        r'x\.com/([^/\s"\']+)'
    ],
    'instagram': [
        r'instagram\.com/([^/\s"\']+)'
    ],
    'facebook': [
        r'facebook\.com/([^/\s"\']+)',
        r'fb\.com/([^/\s"\']+)'
    ],
    'youtube': [
        r'youtube\.com/c/([^/\s"\']+)',
        r'youtube\.com/channel/([^/\s"\']+)',
        r'youtube\.com/user/([^/\s"\']+)',
        r'youtube\.com/@([^/\s"\']+)'
    ],
    'github': [
        r'github\.com/([^/\s"\']+)'
    ]
}

def fetch_html(url, timeout=20, verify_ssl=False):
    """Web sitesinden HTML içeriğini çeker"""
    try:
        # URL'yi parse et
        from urllib.parse import urlparse
        parsed = urlparse(url)
        base_domain = f"{parsed.scheme}://{parsed.netloc}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',  # Bazı siteler keep-alive bekliyor
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': base_domain
        }

        # SSL uyarısını bastır
        import urllib3
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Daha toleranslı HTTPAdapter
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=10,
            max_retries=1
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update(headers)

        response = session.get(url, timeout=timeout, allow_redirects=True, verify=verify_ssl)

        # 500 hatası olsa bile HTML varsa kullan (bazı siteler hata verse de içerik döndürür)
        response.encoding = response.apparent_encoding
        html_content = response.text

        # Session'ı kapat
        session.close()

        # HTML içeriği varsa başarılı sayalım (status code'a bakmadan)
        if html_content and len(html_content) > 1000:  # En az 1KB HTML olmalı
            if response.status_code != 200:
                print(f"⚠️  HTTP {response.status_code} ancak HTML içeriği alındı")
            return html_content

        # HTML yoksa veya çok küçükse hata ver
        response.raise_for_status()
        return html_content

    except requests.RequestException as e:
        print(f"❌ HTML çekme hatası: {e}")
        return None

def follow_redirect(url, timeout=10):
    """Redirect linkini takip edip gerçek URL'i döndürür"""
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, verify=False)
        return response.url
    except:
        return url

def extract_social_links(html, base_url):
    """HTML'den sosyal medya linklerini çıkarır"""
    soup = BeautifulSoup(html, 'html.parser')
    social_links = {
        'linkedin': '',
        'x': '',
        'instagram': '',
        'facebook': '',
        'youtube': '',
        'github': ''
    }

    # Tüm linkleri bul
    all_links = soup.find_all('a', href=True)

    # Redirect linkleri için kontrol (/link/ gibi)
    redirect_links = {}
    for link in all_links:
        href = link.get('href', '')
        href_lower = href.lower()

        # /link/ redirect pattern'lerini kontrol et
        if '/link/' in href_lower:
            if 'linkedin' in href_lower:
                redirect_links['linkedin'] = urljoin(base_url, href)
            elif 'facebook' in href_lower or 'fb' in href_lower:
                redirect_links['facebook'] = urljoin(base_url, href)
            elif 'twitter' in href_lower or href_lower.endswith('/link/x'):
                redirect_links['x'] = urljoin(base_url, href)
            elif 'instagram' in href_lower:
                redirect_links['instagram'] = urljoin(base_url, href)
            elif 'youtube' in href_lower:
                redirect_links['youtube'] = urljoin(base_url, href)
            elif 'github' in href_lower:
                redirect_links['github'] = urljoin(base_url, href)

    for link in all_links:
        href = link.get('href', '')

        # Relative URL'leri absolute yap
        if href.startswith('/'):
            href = urljoin(base_url, href)

        # Her sosyal medya platformu için kontrol et
        for platform, patterns in SOCIAL_PATTERNS.items():
            if social_links[platform]:  # Zaten bulunduysa atla
                continue

            for pattern in patterns:
                match = re.search(pattern, href, re.IGNORECASE)
                if match:
                    # Temiz URL oluştur
                    if platform == 'linkedin':
                        if 'company' in href:
                            social_links[platform] = f"https://linkedin.com/company/{match.group(1)}"
                        else:
                            social_links[platform] = f"https://linkedin.com/in/{match.group(1)}"
                    elif platform == 'x':
                        social_links[platform] = f"https://x.com/{match.group(1)}"
                    elif platform == 'instagram':
                        social_links[platform] = f"https://instagram.com/{match.group(1)}"
                    elif platform == 'facebook':
                        social_links[platform] = f"https://facebook.com/{match.group(1)}"
                    elif platform == 'youtube':
                        # YouTube URL formatını koru
                        if 'channel' in href:
                            social_links[platform] = f"https://youtube.com/channel/{match.group(1)}"
                        elif 'user' in href:
                            social_links[platform] = f"https://youtube.com/user/{match.group(1)}"
                        elif '@' in href:
                            social_links[platform] = f"https://youtube.com/@{match.group(1)}"
                        else:
                            social_links[platform] = f"https://youtube.com/c/{match.group(1)}"
                    elif platform == 'github':
                        social_links[platform] = f"https://github.com/{match.group(1)}"

                    print(f"✅ {platform.capitalize()}: {social_links[platform]}")
                    break

    # Redirect linkleri varsa takip et
    if redirect_links:
        print(f"\n🔄 {len(redirect_links)} redirect linki bulundu, takip ediliyor...")
        for platform, redirect_url in redirect_links.items():
            if not social_links[platform]:  # Henüz bulunmadıysa
                try:
                    real_url = follow_redirect(redirect_url, timeout=10)
                    social_links[platform] = real_url
                    print(f"✅ {platform.capitalize()} (redirect): {real_url}")
                except Exception as e:
                    print(f"⚠️  {platform.capitalize()} redirect hatası: {e}")

    return social_links

def update_company_json(json_path, social_links, dry_run=False):
    """JSON dosyasını sosyal medya linkleriyle günceller"""
    try:
        # JSON dosyasını oku
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Mevcut değerleri sakla
        old_social = data.get('social', {}).copy()

        # Yeni değerleri güncelle (sadece boş olanları - mevcut linklere DOKUNMA)
        updated = False
        for platform, link in social_links.items():
            if link and not old_social.get(platform):
                data['social'][platform] = link
                updated = True
                print(f"  📝 {platform} güncellendi: {link}")
            elif link and old_social.get(platform):
                # Mevcut link varsa atla - DOKUNMA
                print(f"  ✓ {platform} zaten var, korunuyor: {old_social.get(platform)}")

        if not updated:
            print("  ℹ️  Güncellenecek yeni link bulunamadı")
            return False

        # Dosyayı kaydet
        if not dry_run:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Dosya güncellendi: {json_path}")
        else:
            print(f"🔍 DRY RUN: Dosya güncellenmedi (--dry-run)")

        return True

    except Exception as e:
        print(f"❌ JSON güncelleme hatası: {e}")
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Sosyal medya linklerini web sitesinden çeker ve JSON dosyasını günceller')
    parser.add_argument('json_file', help='Güncellenecek JSON dosyası (örn: akgun.json)')
    parser.add_argument('--dry-run', action='store_true', help='Sadece göster, dosyayı güncelleme')
    parser.add_argument('--timeout', type=int, default=10, help='HTTP timeout (saniye)')
    parser.add_argument('--verify-ssl', action='store_true', help='SSL sertifikasını doğrula')

    args = parser.parse_args()

    # JSON dosyasını bul
    json_path = Path(args.json_file)
    if not json_path.exists():
        # public/data/company/ içinde ara
        alt_path = Path('public/data/company') / json_path.name
        if alt_path.exists():
            json_path = alt_path
        else:
            print(f"❌ Dosya bulunamadı: {args.json_file}")
            return 1

    print(f"📂 Dosya: {json_path}")

    # JSON dosyasını oku
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ JSON okuma hatası: {e}")
        return 1

    # Web adresini al
    web_url = data.get('contact', {}).get('web', '')
    if not web_url:
        print("❌ Web adresi bulunamadı (contact.web)")
        return 1

    print(f"🌐 Web Sitesi: {web_url}")
    print(f"\n🔍 Sosyal medya linkleri aranıyor...\n")

    # HTML'i çek
    html = fetch_html(web_url, timeout=args.timeout, verify_ssl=args.verify_ssl)
    if not html:
        return 1

    # Sosyal medya linklerini çıkar
    social_links = extract_social_links(html, web_url)

    # Bulunan linkleri göster
    found_count = sum(1 for link in social_links.values() if link)
    print(f"\n📊 Toplam {found_count} sosyal medya linki bulundu\n")

    if found_count == 0:
        print("ℹ️  Hiç sosyal medya linki bulunamadı")
        return 0

    # JSON'u güncelle
    print("📝 JSON dosyası güncelleniyor...\n")
    success = update_company_json(json_path, social_links, dry_run=args.dry_run)

    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
