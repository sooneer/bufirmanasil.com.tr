import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { Title, Meta } from '@angular/platform-browser';
import { isPlatformBrowser, DOCUMENT } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class SeoService {

  constructor(
    private title: Title,
    private meta: Meta,
    @Inject(PLATFORM_ID) private platformId: Object,
    @Inject(DOCUMENT) private document: Document
  ) { }

  updateTitle(title: string) {
    this.title.setTitle(title);
  }

  updateMetaTags(config: {
    title?: string;
    description?: string;
    keywords?: string;
    image?: string;
    url?: string;
    type?: string;
  }) {
    if (config.title) {
      this.title.setTitle(config.title);
      this.meta.updateTag({ property: 'og:title', content: config.title });
      this.meta.updateTag({ name: 'twitter:title', content: config.title });
    }

    if (config.description) {
      this.meta.updateTag({ name: 'description', content: config.description });
      this.meta.updateTag({ property: 'og:description', content: config.description });
      this.meta.updateTag({ name: 'twitter:description', content: config.description });
    }

    if (config.keywords) {
      this.meta.updateTag({ name: 'keywords', content: config.keywords });
    }

    if (config.image) {
      this.meta.updateTag({ property: 'og:image', content: config.image });
      this.meta.updateTag({ name: 'twitter:image', content: config.image });
    }

    if (config.url) {
      this.meta.updateTag({ property: 'og:url', content: config.url });
      this.updateCanonicalUrl(config.url);
    }

    if (config.type) {
      this.meta.updateTag({ property: 'og:type', content: config.type });
    }
  }

  // Sayfa bazlı SEO konfigürasyonları
  setHomePage() {
    this.updateMetaTags({
      title: 'Bu Firma Nasıl? - Şirket Değerlendirme ve İnceleme Platformu',
      description: 'Türkiye\'deki şirketler hakkında çalışan deneyimleri, maaş bilgileri ve detaylı incelemeler. İş arayan adaylar için güvenilir şirket rehberi.',
      keywords: 'şirket değerlendirme, çalışan yorumları, maaş bilgileri, iş deneyimleri, şirket inceleme, kariyer, iş arama, Türkiye şirketleri',
      url: 'https://bufirmanasil.com.tr',
      type: 'website'
    });
  }

  setCompanyPage(companyName: string, companyDescription?: string) {
    const title = `${companyName} - Çalışan Yorumları ve Şirket İncelemesi | Bu Firma Nasıl?`;
    const description = companyDescription
      ? `${companyName} hakkında çalışan deneyimleri, maaş bilgileri ve detaylı şirket incelemesi. ${companyDescription}`
      : `${companyName} hakkında çalışan deneyimleri, maaş bilgileri ve detaylı şirket incelemesi.`;

    this.updateMetaTags({
      title,
      description,
      keywords: `${companyName}, şirket değerlendirme, çalışan yorumları, maaş bilgileri, iş deneyimleri`,
      url: `https://bufirmanasil.com.tr/company/${this.slugify(companyName)}`,
      type: 'article'
    });
  }

  setCompanyListPage() {
    this.updateMetaTags({
      title: 'Şirket Listesi - Tüm Firmalar | Bu Firma Nasıl?',
      description: 'Türkiye\'deki tüm şirketlerin listesi. Çalışan yorumları ve değerlendirmeleri ile birlikte şirket bilgileri.',
      keywords: 'şirket listesi, Türkiye şirketleri, firma listesi, şirket rehberi, çalışan yorumları',
      url: 'https://bufirmanasil.com.tr/company-list',
      type: 'website'
    });

    // Şirket listesi için CollectionPage structured data
    const structuredData = {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      'name': 'Şirket Listesi',
      'description': 'Türkiye\'deki tüm şirketlerin listesi',
      'url': 'https://bufirmanasil.com.tr/company-list',
      'breadcrumb': {
        '@type': 'BreadcrumbList',
        'itemListElement': [
          {
            '@type': 'ListItem',
            'position': 1,
            'name': 'Ana Sayfa',
            'item': 'https://bufirmanasil.com.tr'
          },
          {
            '@type': 'ListItem',
            'position': 2,
            'name': 'Şirket Listesi',
            'item': 'https://bufirmanasil.com.tr/company-list'
          }
        ]
      }
    };

    this.updateStructuredData(structuredData);
  }

  setAboutPage() {
    this.updateMetaTags({
      title: 'Hakkımızda - Bu Firma Nasıl? Platformu',
      description: 'Bu Firma Nasıl? platformu hakkında bilgiler. Misyonumuz, vizyonumuz ve şirket değerlendirme sistemimiz.',
      keywords: 'hakkımızda, bu firma nasıl, platform bilgileri, misyon, vizyon',
      url: 'https://bufirmanasil.com.tr/about',
      type: 'website'
    });
  }

  setContactPage() {
    this.updateMetaTags({
      title: 'İletişim - Bu Firma Nasıl?',
      description: 'Bu Firma Nasıl? platformu ile iletişime geçin. Sorularınız, önerileriniz ve geri bildirimleriniz için bizimle iletişime geçebilirsiniz.',
      keywords: 'iletişim, contact, geri bildirim, öneriler, destek',
      url: 'https://bufirmanasil.com.tr/contact',
      type: 'website'
    });
  }

  setSektorKodlariPage() {
    this.updateMetaTags({
      title: 'Sektör Kodları - NACE Kodları ve Açıklamaları | Bu Firma Nasıl?',
      description: 'NACE (Avrupa Topluluğunda Ekonomik Faaliyetlerin İstatistiki Sınıflaması) sektör kodları ve detaylı açıklamaları. Tüm sektör kodlarını arayabilir ve inceleyebilirsiniz.',
      keywords: 'sektör kodları, NACE kodları, ekonomik faaliyet sınıflaması, sektör listesi, faaliyet kodları, iş sektörleri',
      url: 'https://bufirmanasil.com.tr/sector-codes',
      type: 'website'
    });

    // Sektör kodları için Dataset structured data
    const structuredData = {
      '@context': 'https://schema.org',
      '@type': 'Dataset',
      'name': 'NACE Sektör Kodları',
      'description': 'Avrupa Topluluğunda Ekonomik Faaliyetlerin İstatistiki Sınıflaması (NACE) kodları tam listesi',
      'url': 'https://bufirmanasil.com.tr/sector-codes',
      'keywords': ['NACE', 'sektör kodları', 'ekonomik faaliyet', 'sınıflandırma'],
      'license': 'https://creativecommons.org/publicdomain/zero/1.0/',
      'creator': {
        '@type': 'Organization',
        'name': 'Bu Firma Nasıl?',
        'url': 'https://bufirmanasil.com.tr'
      }
    };

    this.updateStructuredData(structuredData);
  }

  private slugify(text: string): string {
    return text
      .toLowerCase()
      .replace(/[^a-z0-9 -]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim();
  }

  // Canonical URL güncelleme
  private updateCanonicalUrl(url: string) {
    if (!isPlatformBrowser(this.platformId)) return;

    let link: HTMLLinkElement | null = this.document.querySelector('link[rel="canonical"]');
    if (link) {
      link.setAttribute('href', url);
    } else {
      link = this.document.createElement('link');
      link.setAttribute('rel', 'canonical');
      link.setAttribute('href', url);
      this.document.head.appendChild(link);
    }
  }

  // Structured Data (JSON-LD) güncelleme
  private updateStructuredData(data: any) {
    if (!isPlatformBrowser(this.platformId)) return;

    // Mevcut structured data scriptini kaldır
    const existingScript = this.document.querySelector('script[type="application/ld+json"][data-dynamic="true"]');
    if (existingScript) {
      existingScript.remove();
    }

    // Yeni structured data ekle
    const script = this.document.createElement('script');
    script.type = 'application/ld+json';
    script.setAttribute('data-dynamic', 'true');
    script.text = JSON.stringify(data);
    this.document.head.appendChild(script);
  }

  // Gelişmiş şirket sayfası SEO (Structured Data ile)
  setCompanyPageWithStructuredData(companyData: {
    name: string;
    about?: string;
    logo?: string;
    foundationYear?: number;
    sector?: string[];
    web?: string;
    email?: string;
    phone?: string;
    address?: string;
    linkedin?: string;
    slug: string;
  }) {
    const title = `${companyData.name} - Şirket Bilgileri, İletişim ve Hakkında | Bu Firma Nasıl?`;
    const description = companyData.about
      ? `${companyData.name} şirketi hakkında detaylı bilgiler. ${companyData.about.substring(0, 150)}...`
      : `${companyData.name} şirketi hakkında detaylı bilgiler, iletişim bilgileri ve şirket profili.`;

    const keywords = [
      companyData.name,
      'şirket bilgileri',
      'firma profili',
      'iletişim bilgileri',
      ...(companyData.sector || [])
    ].join(', ');

    const url = `https://bufirmanasil.com.tr/company/${companyData.slug}`;
    const imageUrl = companyData.logo ? `https://bufirmanasil.com.tr/${companyData.logo}` : 'https://bufirmanasil.com.tr/img/logo.svg';

    // Temel meta tagları güncelle
    this.updateMetaTags({
      title,
      description,
      keywords,
      url,
      type: 'article',
      image: imageUrl
    });

    // Structured Data (Organization Schema)
    const structuredData: any = {
      '@context': 'https://schema.org',
      '@type': 'Organization',
      'name': companyData.name,
      'url': url,
      'logo': imageUrl,
      'description': companyData.about || `${companyData.name} şirketi hakkında bilgiler.`
    };

    if (companyData.foundationYear) {
      structuredData.foundingDate = companyData.foundationYear.toString();
    }

    if (companyData.email) {
      structuredData.email = companyData.email;
    }

    if (companyData.phone) {
      structuredData.telephone = companyData.phone;
    }

    if (companyData.address) {
      structuredData.address = {
        '@type': 'PostalAddress',
        'addressCountry': 'TR',
        'addressLocality': companyData.address
      };
    }

    // Sosyal medya hesapları
    const sameAs = [];
    if (companyData.linkedin) sameAs.push(companyData.linkedin);
    if (companyData.web) sameAs.push(companyData.web);
    if (sameAs.length > 0) {
      structuredData.sameAs = sameAs;
    }

    this.updateStructuredData(structuredData);

    // Breadcrumb Structured Data
    this.addBreadcrumbStructuredData([
      { name: 'Ana Sayfa', url: 'https://bufirmanasil.com.tr' },
      { name: 'Şirketler', url: 'https://bufirmanasil.com.tr/company-list' },
      { name: companyData.name, url: url }
    ]);
  }

  // Breadcrumb Structured Data ekleme
  private addBreadcrumbStructuredData(items: Array<{ name: string, url: string }>) {
    if (!isPlatformBrowser(this.platformId)) return;

    const breadcrumbData = {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      'itemListElement': items.map((item, index) => ({
        '@type': 'ListItem',
        'position': index + 1,
        'name': item.name,
        'item': item.url
      }))
    };

    // Mevcut breadcrumb scriptini kaldır
    const existingScript = this.document.querySelector('script[type="application/ld+json"][data-breadcrumb="true"]');
    if (existingScript) {
      existingScript.remove();
    }

    // Yeni breadcrumb ekle
    const script = this.document.createElement('script');
    script.type = 'application/ld+json';
    script.setAttribute('data-breadcrumb', 'true');
    script.text = JSON.stringify(breadcrumbData);
    this.document.head.appendChild(script);
  }
}
