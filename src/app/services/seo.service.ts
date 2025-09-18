import { Injectable } from '@angular/core';
import { Title, Meta } from '@angular/platform-browser';

@Injectable({
  providedIn: 'root'
})
export class SeoService {

  constructor(
    private title: Title,
    private meta: Meta
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
      this.meta.updateTag({ rel: 'canonical', href: config.url });
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
  }

  private slugify(text: string): string {
    return text
      .toLowerCase()
      .replace(/[^a-z0-9 -]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim();
  }
}
