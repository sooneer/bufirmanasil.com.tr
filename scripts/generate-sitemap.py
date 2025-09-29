#!/usr/bin/env python3
"""
Sitemap Generator
Generates sitemap.xml from companies.json
"""

import json
from datetime import date
from pathlib import Path

def generate_sitemap():
    # Paths
    root_dir = Path(__file__).parent.parent
    companies_file = root_dir / 'public' / 'data' / 'companies.json'
    sitemap_file = root_dir / 'docs' / 'sitemap.xml'

    # Read companies
    with open(companies_file, 'r', encoding='utf-8') as f:
        companies = json.load(f)

    # Current date for lastmod
    today = date.today().isoformat()

    # Start XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
        '        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">',
        '',
        '  <!-- Ana Sayfa -->',
        '  <url>',
        '    <loc>https://bufirmanasil.com.tr/</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
        '',
        '  <!-- Ana Sayfa (Home) -->',
        '  <url>',
        '    <loc>https://bufirmanasil.com.tr/home</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.9</priority>',
        '  </url>',
        '',
        '  <!-- Hakkımızda -->',
        '  <url>',
        '    <loc>https://bufirmanasil.com.tr/about</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.8</priority>',
        '  </url>',
        '',
        '  <!-- İletişim -->',
        '  <url>',
        '    <loc>https://bufirmanasil.com.tr/contact</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.8</priority>',
        '  </url>',
        '',
        '  <!-- Şirket Listesi -->',
        '  <url>',
        '    <loc>https://bufirmanasil.com.tr/company-list</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>0.9</priority>',
        '  </url>',
        '',
        '  <!-- Sektör Kodları -->',
        '  <url>',
        '    <loc>https://bufirmanasil.com.tr/sector-codes</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.7</priority>',
        '  </url>',
        '',
        '  <!-- Gizlilik Politikası -->',
        '  <url>',
        '    <loc>https://bufirmanasil.com.tr/privacy</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>yearly</changefreq>',
        '    <priority>0.3</priority>',
        '  </url>',
        '',
        '  <!-- Kullanım Şartları -->',
        '  <url>',
        '    <loc>https://bufirmanasil.com.tr/terms</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>yearly</changefreq>',
        '    <priority>0.3</priority>',
        '  </url>',
        '',
        '  <!-- Çerez Politikası -->',
        '  <url>',
        '    <loc>https://bufirmanasil.com.tr/cookies</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>yearly</changefreq>',
        '    <priority>0.3</priority>',
        '  </url>',
        '',
        '  <!-- Şirket Sayfaları -->',
    ]

    # Add company URLs
    for company in companies:
        slug = company.get('slug', '')
        if slug:
            xml_lines.extend([
                '  <url>',
                f'    <loc>https://bufirmanasil.com.tr/company/{slug}</loc>',
                f'    <lastmod>{today}</lastmod>',
                '    <changefreq>monthly</changefreq>',
                '    <priority>0.6</priority>',
                '  </url>',
                '',
            ])

    # Close XML
    xml_lines.append('</urlset>')

    # Write sitemap
    with open(sitemap_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))

    print(f"✅ Sitemap oluşturuldu: {sitemap_file}")
    print(f"📊 Toplam URL sayısı: {9 + len(companies)}")
    print(f"   - Statik sayfalar: 9")
    print(f"   - Şirket sayfaları: {len(companies)}")

if __name__ == '__main__':
    generate_sitemap()
