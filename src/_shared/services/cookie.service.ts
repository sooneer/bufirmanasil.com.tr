import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { BehaviorSubject } from 'rxjs';

export interface CookieConsent {
  necessary: boolean;
  analytics: boolean;
  marketing: boolean;
  timestamp: Date;
}

@Injectable({
  providedIn: 'root'
})
export class CookieService {
  private readonly CONSENT_KEY = 'cookie-consent';
  private consentSubject = new BehaviorSubject<CookieConsent | null>(null);
  public consent$ = this.consentSubject.asObservable();
  private isBrowser: boolean;

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {
    this.isBrowser = isPlatformBrowser(this.platformId);
    if (this.isBrowser) {
      this.loadConsent();
    }
  }

  private loadConsent(): void {
    if (!this.isBrowser) return;
    
    try {
      const stored = localStorage.getItem(this.CONSENT_KEY);
      if (stored) {
        const consent = JSON.parse(stored);
        // Tarihi Date objesine çevir
        consent.timestamp = new Date(consent.timestamp);
        this.consentSubject.next(consent);
      }
    } catch (e) {
      console.error('Cookie consent parse error:', e);
    }
  }

  saveConsent(consent: Omit<CookieConsent, 'timestamp'>): void {
    if (!this.isBrowser) return;
    
    const fullConsent: CookieConsent = {
      ...consent,
      necessary: true, // Zorunlu çerezler her zaman aktif
      timestamp: new Date()
    };

    try {
      localStorage.setItem(this.CONSENT_KEY, JSON.stringify(fullConsent));
      this.consentSubject.next(fullConsent);

      // Google Analytics'i aktif/pasif et
      this.toggleAnalytics(fullConsent.analytics);
      
      // Marketing çerezlerini kontrol et
      this.toggleMarketing(fullConsent.marketing);
    } catch (e) {
      console.error('Cookie consent save error:', e);
    }
  }

  hasConsent(): boolean {
    return this.consentSubject.value !== null;
  }

  getConsent(): CookieConsent | null {
    return this.consentSubject.value;
  }

  revokeConsent(): void {
    if (!this.isBrowser) return;
    
    try {
      localStorage.removeItem(this.CONSENT_KEY);
      this.consentSubject.next(null);
      
      // Tüm çerezleri temizle
      this.clearNonEssentialCookies();
    } catch (e) {
      console.error('Cookie consent revoke error:', e);
    }
  }

  private toggleAnalytics(enabled: boolean): void {
    if (!this.isBrowser) return;
    
    if (typeof gtag !== 'undefined') {
      gtag('consent', 'update', {
        analytics_storage: enabled ? 'granted' : 'denied'
      });
    }
  }

  private toggleMarketing(enabled: boolean): void {
    if (!this.isBrowser) return;
    
    if (typeof gtag !== 'undefined') {
      gtag('consent', 'update', {
        ad_storage: enabled ? 'granted' : 'denied',
        ad_user_data: enabled ? 'granted' : 'denied',
        ad_personalization: enabled ? 'granted' : 'denied'
      });
    }
  }

  private clearNonEssentialCookies(): void {
    if (!this.isBrowser) return;
    
    // Google Analytics çerezlerini temizle
    const cookiesToClear = [
      '_ga', '_ga_', '_gid', '_gat', '_gtag_GA_',
      '__utma', '__utmb', '__utmc', '__utmt', '__utmz'
    ];

    cookiesToClear.forEach(cookieName => {
      try {
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=${window.location.hostname}`;
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.${window.location.hostname}`;
      } catch (e) {
        console.error('Error clearing cookie:', cookieName, e);
      }
    });
  }

  // Çerez tiplerinin açıklamaları
  getCookieTypes() {
    return {
      necessary: {
        name: 'Zorunlu Çerezler',
        description: 'Web sitesinin temel işlevleri için gerekli çerezler. Bu çerezler devre dışı bırakılamaz.',
        always: true
      },
      analytics: {
        name: 'Analitik Çerezler',
        description: 'Web sitesinin performansını analiz etmek ve kullanıcı deneyimini iyileştirmek için kullanılır.',
        always: false
      },
      marketing: {
        name: 'Pazarlama Çerezleri',
        description: 'Kişiselleştirilmiş reklamlar göstermek ve reklam performansını ölçmek için kullanılır.',
        always: false
      }
    };
  }
}

// Global gtag tipini tanımla
declare global {
  function gtag(...args: any[]): void;
}