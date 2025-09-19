import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { URLHelpers } from '../../_helpers/url-helpers';
import { SeoService } from '../../_shared/services/seo.service';

@Component({
  selector: 'app-company-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './company-list.component.html',
  encapsulation: ViewEncapsulation.None,
})
export class CompanyListComponent implements OnInit {
  companies: string[] = [];

  constructor(
    private http: HttpClient,
    private seoService: SeoService
  ) {}

  ngOnInit() {
    // SEO ayarları
    this.seoService.setCompanyListPage();

    this.http.get<string[]>('/data/companies.json').subscribe((data) => {
      console.log(data);
      this.companies = data;
    });
  }

  toFriendlyUrl(company) {
    return URLHelpers.toFriendlyUrl(company);
  }
}
