import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CompanyListItem } from '../../_shared/models/Company';
import { SeoService } from '../../_shared/services/seo.service';

@Component({
  selector: 'app-company-list',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './company-list.component.html',
  encapsulation: ViewEncapsulation.None,
})
export class CompanyListComponent implements OnInit {
  companies: CompanyListItem[] = [];

  constructor(
    private http: HttpClient,
    private seoService: SeoService
  ) {}

  ngOnInit() {
    // SEO ayarları
    this.seoService.setCompanyListPage();

    this.http.get<CompanyListItem[]>('/data/companies.json').subscribe((data) => {
      this.companies = data;
    });
  }
}
