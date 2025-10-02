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
    company_data_dir = root_dir / 'public' / 'data' / 'company'
    sitemap_file = root_dir / 'docs' / 'sitemap.xml'
    sitemap_file_public = root_dir / 'public' / 'sitemap.xml'

    # Get all company JSON files
    company_files = sorted(company_data_dir.glob('*.json'))

    # Extract slugs from filenames
    companies = []
    for company_file in company_files:
        slug = company_file.stem
        companies.append({'slug': slug})

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

    # Write sitemap to both locations
    for output_file in [sitemap_file, sitemap_file_public]:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(xml_lines))
        print(f"✅ Sitemap oluşturuldu: {output_file}")
    print(f"📊 Toplam URL sayısı: {9 + len(companies)}")
    print(f"   - Statik sayfalar: 9")
    print(f"   - Şirket sayfaları: {len(companies)}")

if __name__ == '__main__':
    generate_sitemap()
