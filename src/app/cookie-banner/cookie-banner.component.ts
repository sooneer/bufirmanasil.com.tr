import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CookieService, CookieConsent } from '../services/cookie.service';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-cookie-banner',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './cookie-banner.component.html',
  styleUrls: ['./cookie-banner.component.scss']
})
export class CookieBannerComponent implements OnInit, OnDestroy {
  showBanner = true; // Başlangıçta true, consent varsa false olacak
  showDetails = false;
  cookieTypes: any;
  
  preferences = {
    analytics: false,
    marketing: false
  };

  private destroy$ = new Subject<void>();

  constructor(private cookieService: CookieService) {
    // Constructor'da hızlıca kontrol et
    if (this.cookieService.hasConsent()) {
      this.showBanner = false;
    }
  }

  ngOnInit(): void {
    this.cookieTypes = this.cookieService.getCookieTypes();
    
    // Hemen consent durumunu kontrol et
    const currentConsent = this.cookieService.getConsent();
    this.showBanner = !currentConsent;
    
    if (currentConsent) {
      this.preferences = {
        analytics: currentConsent.analytics,
        marketing: currentConsent.marketing
      };
    }
    
    // Observable'ı dinle ama sadece değişiklikler için
    this.cookieService.consent$
      .pipe(takeUntil(this.destroy$))
      .subscribe(consent => {
        if (consent) {
          this.showBanner = false;
          this.preferences = {
            analytics: consent.analytics,
            marketing: consent.marketing
          };
        }
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  acceptAll(): void {
    this.cookieService.saveConsent({
      necessary: true,
      analytics: true,
      marketing: true
    });
    this.closeBanner();
  }

  acceptSelected(): void {
    this.cookieService.saveConsent({
      necessary: true,
      analytics: this.preferences.analytics,
      marketing: this.preferences.marketing
    });
    this.closeBanner();
  }

  rejectAll(): void {
    this.cookieService.saveConsent({
      necessary: true,
      analytics: false,
      marketing: false
    });
    this.closeBanner();
  }

  toggleDetails(): void {
    this.showDetails = !this.showDetails;
  }

  private closeBanner(): void {
    this.showBanner = false;
    this.showDetails = false;
  }
}