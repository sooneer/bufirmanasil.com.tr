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
  showBanner = false;
  showDetails = false;
  cookieTypes: any;
  
  preferences = {
    analytics: false,
    marketing: false
  };

  private destroy$ = new Subject<void>();

  constructor(private cookieService: CookieService) {}

  ngOnInit(): void {
    this.cookieTypes = this.cookieService.getCookieTypes();
    
    this.cookieService.consent$
      .pipe(takeUntil(this.destroy$))
      .subscribe(consent => {
        this.showBanner = !consent;
        if (consent) {
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