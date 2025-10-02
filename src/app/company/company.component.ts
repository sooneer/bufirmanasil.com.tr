import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit, ViewEncapsulation, Renderer2, ElementRef, AfterViewInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Company } from '../../_shared/models/Company';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { DomSanitizer } from '@angular/platform-browser';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { GiscusComponent } from '../../_shared/components/giscus.component';
import { SeoService } from '../../_shared/services/seo.service';
import { PLATFORM_ID } from '@angular/core';

@Component({
  selector: 'app-company',
  standalone: true,
  imports: [CommonModule, GiscusComponent],
  templateUrl: './company.component.html',
  styleUrl: './company.component.scss',
  animations: [
    trigger('fadeInOut', [
      state('void', style({ opacity: 0, transform: 'translateY(20px)' })),
      transition('void <=> *', animate('1000ms ease-in-out')),
    ]),
  ],
  encapsulation: ViewEncapsulation.None,
})
export class CompanyComponent implements OnInit, AfterViewInit {
  CompanyUrl?: string;
  Company: Company | null = null;
  showAllClients: boolean = false;
  readonly maxVisibleClients = 8;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private http: HttpClient,
    private sanitizer: DomSanitizer,
    private seoService: SeoService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) { }

  ngOnInit() {
    this.route.url.subscribe((event) => {
      //console.log(event); // It's an array remember [0]
      this.CompanyUrl = event[1]?.path;
      this.LoadCompany();
    });
  }

  LoadCompany() {
    if (this.CompanyUrl && this.CompanyUrl !== 'company') {
      console.log('Loading company:', this.CompanyUrl, 'Platform is browser:', isPlatformBrowser(this.platformId));

      if (isPlatformBrowser(this.platformId)) {
        // Browser'da normal HTTP request yap
        this.http
          .get<Company>('/data/company/' + this.CompanyUrl + '.json')
          .subscribe((data) => {
            this.Company = data;

            // Initialize Google AdSense after content updates
            setTimeout(() => this.initializeAds(), 0);

            // SEO meta taglerini güncelle - Zengin structured data ile
            if (this.Company) {
              this.seoService.setCompanyPageWithStructuredData({
                name: this.Company.name,
                about: this.Company.about,
                logo: this.Company.logo,
                foundationYear: this.Company.foundationYear,
                sector: this.Company.sector,
                web: this.Company.contact?.web,
                email: this.Company.contact?.email,
                phone: this.Company.contact?.phone,
                address: this.Company.contact?.address,
                linkedin: this.Company.social?.linkedin,
                slug: this.CompanyUrl
              });
            }
          });
      } else {
        // Server'da dummy data kullan
        console.log('Server-side rendering detected, using dummy data');
        this.Company = {
          name: this.CompanyUrl.replace('-', ' ').toUpperCase(),
          logo: `/img/company/${this.CompanyUrl}.svg`,
          tagline: 'Şirket açıklaması',
          foundationYear: 2000,
          about: `${this.CompanyUrl} hakkında bilgiler`,
          sector: ['Teknoloji'],
          clients: [],
          contact: {
            web: 'https://example.com',
            email: 'info@example.com',
            phone: '+90 212 123 45 67',
            address: 'İstanbul'
          },
          social: {
            linkedin: '',
            x: '',
            instagram: '',
            facebook: '',
            youtube: '',
            github: ''
          }
        };

        // SEO meta taglerini güncelle - Zengin structured data ile
        this.seoService.setCompanyPageWithStructuredData({
          name: this.Company.name,
          about: this.Company.about,
          logo: this.Company.logo,
          foundationYear: this.Company.foundationYear,
          sector: this.Company.sector,
          web: this.Company.contact?.web,
          email: this.Company.contact?.email,
          phone: this.Company.contact?.phone,
          address: this.Company.contact?.address,
          linkedin: this.Company.social?.linkedin,
          slug: this.CompanyUrl
        });

        // Initialize ads on client only (noop on server)
        setTimeout(() => this.initializeAds(), 0);
      }
    }
  }

  ngAfterViewInit(): void {
    // Ensure ads are initialized after first render on the browser
    this.initializeAds();
  }

  private initializeAds(): void {
    if (!isPlatformBrowser(this.platformId)) {
      return;
    }
    try {
      const w = window as any;
      w.adsbygoogle = w.adsbygoogle || [];
      const adElements = document.querySelectorAll('ins.adsbygoogle');
      adElements.forEach(() => {
        try {
          w.adsbygoogle.push({});
        } catch (e) {
          // ignore individual push errors to avoid breaking the page
        }
      });
    } catch (e) {
      // ignore
    }
  }

  toggleShowAllClients() {
    this.showAllClients = !this.showAllClients;
  }

  getVisibleClients() {
    if (!this.Company?.clients) return [];

    if (this.showAllClients || this.Company.clients.length <= this.maxVisibleClients) {
      return this.Company.clients;
    }

    return this.Company.clients.slice(0, this.maxVisibleClients);
  }

  hasMoreClients(): boolean {
    return !!(this.Company?.clients && this.Company.clients.length > this.maxVisibleClients);
  }

  getSafeUrl(url: string) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }

  removeProtocol(url: string): string {
    if (!url) return '';
    return url.replace(/^https?:\/\//, '');
  }
}
