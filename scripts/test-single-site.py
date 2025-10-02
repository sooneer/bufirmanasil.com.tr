#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tek bir web sitesini test et - sosyal medya linklerini ara
"""

import requests
from bs4 import BeautifulSoup
import re
import urllib3

# SSL uyarısını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://www.akgun.com.tr'
print(f'🌐 Web Sitesi: {url}')
print(f'📥 HTML içeriği indiriliyor...\n')

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=15, verify=False)
    html = response.text

    print(f'✅ HTML boyutu: {len(html):,} karakter')
    print(f'📄 Status Code: {response.status_code}\n')

    # Tüm linkleri bul
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find_all('a', href=True)

    print(f'🔗 Toplam {len(all_links)} link bulundu\n')

    # Sosyal medya anahtar kelimeleri
    social_keywords = ['linkedin', 'facebook', 'twitter', 'x.com', 'instagram', 'youtube', 'github']

    print('🔍 Sosyal medya linkleri aranıyor...\n')
    social_links = []

    for link in all_links:
        href = link.get('href', '')
        href_lower = href.lower()

        for keyword in social_keywords:
            if keyword in href_lower:
                social_links.append(href)
                print(f'  ✓ {href}')
                break

    if not social_links:
        print('  ❌ Hiç sosyal medya linki bulunamadı')
        print('\n📋 Sitedeki ilk 30 link:')
        print('-' * 80)
        for i, link in enumerate(all_links[:30], 1):
            href = link.get('href', '')
            text = link.get_text(strip=True)[:40]
            print(f'  {i:2}. {href[:70]:<70} | {text}')

        # Meta tag'leri kontrol et
        print('\n🔍 Meta tag\'leri kontrol ediliyor...')
        meta_tags = soup.find_all('meta')
        for meta in meta_tags:
            if 'og:' in str(meta) or 'twitter:' in str(meta):
                print(f'  • {meta}')
    else:
        print(f'\n✅ Toplam {len(social_links)} sosyal medya linki bulundu!')

except Exception as e:
    print(f'❌ Hata: {e}')
    import traceback
    traceback.print_exc()
