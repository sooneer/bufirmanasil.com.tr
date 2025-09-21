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
export class CompanyComponent implements OnInit {
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
  ) {}

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

            // SEO meta taglerini güncelle
            if (this.Company) {
              this.seoService.setCompanyPage(this.Company.name, this.Company.about);
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
          services: [],
          softwares: [],
          solutions: [],
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

        // SEO meta taglerini güncelle
        this.seoService.setCompanyPage(this.Company.name, this.Company.about);
      }
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
}
