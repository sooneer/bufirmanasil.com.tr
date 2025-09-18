# Bu Firma Nasıl? 🏢

**Bu Firma Nasıl?** platformu, Türkiye'deki şirketler hakkında kapsamlı bilgi sunan, modern ve kullanıcı dostu bir web uygulamasıdır. Angular ile geliştirilmiş olan bu platform, şirket bilgileri, sektör kodları ve iş dünyası hakkında detaylı veriler sunmaktadır.

![Angular](https://img.shields.io/badge/Angular-19-red?style=for-the-badge&logo=angular)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 🌐 Demo

**Canlı Site:** [https://bufirmanasil.com.tr](https://bufirmanasil.com.tr)

## ✨ Özellikler

### 🏢 **Şirket Bilgileri**
- **Detaylı Şirket Profilleri**: Logo, kuruluş yılı, sektör, hizmetler
- **İletişim Bilgileri**: Adres, telefon, e-posta, sosyal medya
- **Finansal Bilgiler**: BIST kodları, KAP linkleri
- **Müşteri Referansları**: Şirketlerin çalıştığı kurumlar

### 📊 **Sektör Kodları**
- **4000+ NACE Sektör Kodu**: Tam liste ve açıklamalar
- **Gelişmiş Arama**: Kod ve açıklama bazlı filtreleme
- **JSON Export**: Tüm verileri indirme özelliği
- **Responsive Tasarım**: Mobil ve desktop uyumlu

### 🎨 **Modern UI/UX**
- **Responsive Design**: Tüm cihazlarda mükemmel görünüm
- **Dark/Light Mode**: Kullanıcı tercihi
- **Smooth Animations**: Modern geçiş efektleri
- **Mobile-First**: Mobil öncelikli tasarım

### 🔍 **SEO & Performance**
- **Server-Side Rendering (SSR)**: Hızlı yükleme ve SEO
- **Meta Tags**: Dinamik SEO optimizasyonu
- **Open Graph**: Sosyal medya paylaşım desteği
- **Structured Data**: Schema.org markup

## 🛠️ Teknoloji Stack

### **Frontend**
- **Angular 19**: Modern component-based framework
- **TypeScript 5.6**: Type-safe development
- **SCSS**: Advanced styling
- **Angular Universal**: SSR support

### **Deployment & Tools**
- **GitHub Pages**: Static hosting
- **PowerShell**: Automated deployment scripts
- **Angular CLI**: Development tools
- **ESLint**: Code quality

### **SEO & Analytics**
- **Google Analytics**: Traffic tracking
- **Structured Data**: Rich snippets
- **Sitemap.xml**: Search engine optimization
- **Robots.txt**: Crawler guidance

## 🚀 Kurulum

### **Gereksinimler**
- Node.js 18+ 
- npm 9+
- Angular CLI 19+

### **Proje Kurulumu**
```bash
# Repository'yi klonlayın
git clone https://github.com/sooneer/bufirmanasil.com.tr.git
cd bufirmanasil.com.tr

# Bağımlılıkları yükleyin
npm install

# Development server'ı başlatın
ng serve

# Tarayıcıda açın: http://localhost:4200
```

### **Build & Deploy**
```bash
# Production build
npm run build:prod

# Belirli bir klasöre deploy
.\deploy.ps1 -TargetPath "C:\inetpub\wwwroot"

# GitHub Pages deploy
git push origin main
```

## 📁 Proje Yapısı

```
src/
├── app/
│   ├── components/          # Reusable components
│   ├── pages/              # Page components
│   │   ├── home/           # Ana sayfa
│   │   ├── company/        # Şirket detay sayfaları
│   │   ├── company-list/   # Şirket listesi
│   │   ├── sector-codes/   # Sektör kodları
│   │   ├── about/          # Hakkında
│   │   ├── contact/        # İletişim
│   │   ├── privacy/        # Gizlilik Politikası
│   │   ├── terms/          # Kullanım Şartları
│   │   └── cookies/        # Çerez Politikası
│   ├── services/           # Angular services
│   ├── models/             # TypeScript interfaces
│   └── shared/             # Shared utilities
├── assets/                 # Static assets
├── styles/                 # Global styles
└── environments/           # Environment configs

public/
├── data/
│   ├── company/           # Şirket JSON dosyaları
│   └── SektorKodlari.json # Sektör kodları verisi
├── img/                   # Images
├── sitemap.xml           # SEO sitemap
├── robots.txt            # Search engine directives
└── CNAME                 # GitHub Pages domain
```

## 🎯 Ana Sayfalar

| Sayfa | Route | Açıklama |
|-------|-------|----------|
| **Ana Sayfa** | `/` | Platform tanıtımı ve arama |
| **Şirket Listesi** | `/company-list` | Tüm şirketlerin listesi |
| **Şirket Detay** | `/company/:slug` | Şirket detay sayfaları |
| **Sektör Kodları** | `/sector-codes` | NACE kodları ve arama |
| **Hakkında** | `/about` | Platform hakkında bilgi |
| **İletişim** | `/contact` | İletişim formu |
| **Gizlilik** | `/privacy` | KVKK uyumlu gizlilik politikası |
| **Kullanım Şartları** | `/terms` | Platform kullanım kuralları |

## 🔧 Geliştirme Komutları

```bash
# Development server
ng serve                    # http://localhost:4200

# Build commands  
ng build                    # Development build
ng build --configuration production  # Production build

# Testing
ng test                     # Unit tests
ng e2e                      # End-to-end tests

# Code quality
ng lint                     # ESLint check

# Deployment
npm run deploy              # Build + Deploy to default
npm run deploy:to "path"    # Build + Deploy to specific path
```

## 🍪 Çerez & Gizlilik

Platform, KVKK ve GDPR uyumlu çerez yönetimi içerir:

- **Çerez Banner**: Kullanıcı onay sistemi
- **Çerez Kategorileri**: Zorunlu, Analitik, Pazarlama
- **Tercih Yönetimi**: Kullanıcı kontrollü ayarlar
- **Gizlilik Politikası**: Detaylı veri işleme bilgisi

## 📊 Şirket Veri Yapısı

```typescript
interface Company {
  name: string;                    // Şirket adı
  logo: string;                    // Logo yolu
  tagline: string;                 // Slogan
  foundationYear: number;          // Kuruluş yılı
  about: string;                   // Hakkında
  BIST?: {                        // Borsa bilgileri
    code: string;
    KAP: string;
  };
  sector: string[];               // Sektörler
  services: Service[];            // Hizmetler
  clients: string[];              // Müşteriler
  contact: ContactInfo;           // İletişim
  social: SocialMedia;            // Sosyal medya
}
```

## 🎨 Tasarım Sistemi

### **Renk Paleti**
- **Primary**: `#2563eb` (Mavi)
- **Secondary**: `#64748b` (Gri)
- **Success**: `#10b981` (Yeşil)
- **Warning**: `#f59e0b` (Turuncu)
- **Error**: `#ef4444` (Kırmızı)

### **Typography**
- **Font Family**: 'Inter', sans-serif
- **Headings**: Font-weight 600-700
- **Body**: Font-weight 400
- **Small**: Font-weight 300

### **Responsive Breakpoints**
```scss
$mobile: 480px;
$tablet: 768px;
$desktop: 1024px;
$large: 1200px;
```

## 🚀 Deployment

### **GitHub Pages**
```bash
# Otomatik deployment (main branch)
git push origin main

# Manuel deployment
ng build --configuration production
# docs/ klasörü GitHub Pages'e deploy edilir
```

### **Custom Server**
```bash
# PowerShell deployment script
.\deploy.ps1 -TargetPath "docs" -Clean

# Deployment özellikleri:
# ✅ Production build
# ✅ File copying
# ✅ 404.html creation (SPA routing)
# ✅ CNAME file inclusion
```

## 📈 Performance & SEO

### **Core Web Vitals**
- **LCP**: < 2.5s (Largest Contentful Paint)
- **FID**: < 100ms (First Input Delay)  
- **CLS**: < 0.1 (Cumulative Layout Shift)

### **SEO Features**
- Dynamic meta tags
- Structured data (JSON-LD)
- XML sitemap
- Open Graph tags
- Twitter Cards
- Canonical URLs

## 🔒 Güvenlik

- **HTTPS**: SSL/TLS encryption
- **CSP**: Content Security Policy headers
- **KVKK Compliance**: Turkish data protection law
- **GDPR Compliance**: European data protection
- **XSS Protection**: Input sanitization

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📝 Changelog

### v1.0.0 (2025-09-18)
- ✅ İlk platform lansmanı
- ✅ Şirket profilleri sistemi
- ✅ Sektör kodları modülü
- ✅ SEO optimizasyonu
- ✅ KVKK/GDPR uyumlu çerez sistemi
- ✅ Responsive tasarım

## 📄 Lisans

Bu proje [MIT License](LICENSE) altında lisanslanmıştır.

## 📞 İletişim

- **Website**: [https://bufirmanasil.com.tr](https://bufirmanasil.com.tr)
- **Email**: [ben@soneracar.net](mailto:ben@soneracar.net)
- **GitHub**: [https://github.com/sooneer/bufirmanasil.com.tr](https://github.com/sooneer/bufirmanasil.com.tr)

---

**Bu Firma Nasıl?** ile Türkiye'deki şirketler hakkında doğru ve güncel bilgilere kolayca ulaşın! 🚀
